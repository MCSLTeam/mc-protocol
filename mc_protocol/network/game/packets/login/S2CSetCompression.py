from mc_protocol.network.game.packet import Packet, ProtocolDirection, ProtocolState
from mc_protocol.network.packet.varint_processor import VarIntProcessor


class S2CSetCompression(Packet):
    PACKET_ID = 0x03
    PROTOCOL_STATE = ProtocolState.LOGIN
    PROTOCOL_DIRECTION = ProtocolDirection.S2C
    def __init__(self, packet, encryptor=None):
        self.encryptor = encryptor
        self.packet = self.encryptor.deEncryptPacket(packet) if self.encryptor is not None else packet
        
    def getThreshold(self):
        return VarIntProcessor.readVarInt(self.packet)[0]