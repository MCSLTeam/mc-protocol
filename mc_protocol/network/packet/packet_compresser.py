import zlib
from mc_protocol.network.packet.varint_processor import VarIntProcessor

class PacketCompresser:
    def __init__(self, threshold: int):
        self.threshold = threshold

    def compressPacket(self, p: bytes) -> bytes:
        _, packetId, payload = VarIntProcessor.unpackPacket(p)
        body = packetId + payload

        if len(body) < self.threshold:
            dataLength = VarIntProcessor.packVarInt(0)
            packetLength = VarIntProcessor.packVarInt(len(dataLength) + len(body))
            return packetLength + dataLength + body
        compressed = zlib.compress(body)
        dataLength = VarIntProcessor.packVarInt(len(body))
        packetLength = VarIntProcessor.packVarInt(len(dataLength) + len(compressed))
        return packetLength + dataLength + compressed

    def uncompressPacket(self, p: bytes) -> bytes:
        _, dataLength, payload = VarIntProcessor.unpackCompressedPacket(p)
        if dataLength == 0:
            return p

        decompressed = zlib.decompress(payload)
        newPacketLength = VarIntProcessor.packVarInt(len(decompressed))
        return newPacketLength + decompressed
