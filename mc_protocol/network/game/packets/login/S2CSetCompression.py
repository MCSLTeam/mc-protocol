from mc_protocol.network.game.packet import S2CPacket
from mc_protocol.network.packet.varint_processor import VarIntProcessor


class S2CSetCompression(S2CPacket):
    def __init__(self, packet, encryptor=None):
        self.encryptor = encryptor
        self.packet = self.encryptor.deEncryptPacket(packet) if self.encryptor is not None else packet
        
    def getThreshold(self):
        return VarIntProcessor.readVarInt(self.packet)[0]