import zlib

from mc_protocol.network.packet.varint_processor import VarIntProcessor
class PacketCompresser:
    def __init__(self, threshold: int):
        self.threshold = threshold
    def compressPacket(self, p: bytes) -> bytes:
        packetLength, packetId, payload = VarIntProcessor.unpackPacket(p)
        if packetLength < self.threshold:
            return packetLength + VarIntProcessor.packVarInt(0) + packetId + payload
        compressedPacket = zlib.compress(packetId + payload)
        dataLength = VarIntProcessor.packVarInt(len(packetId + payload))
        packetLength = VarIntProcessor.packVarInt(len(dataLength) + len(compressedPacket))

        return packetLength + dataLength + compressedPacket
    def uncompressPacket(self, p: bytes) -> bytes:
        packetLength, dataLength, packetId, payload = VarIntProcessor.unpackCompressedPacket(p)
        return p if dataLength == 0 else packetLength + dataLength + packetId + zlib.decompress(payload)