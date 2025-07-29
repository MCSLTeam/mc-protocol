from mc_protocol.network.game.packet import Packet
from mc_protocol.network.packet.varint_processor import VarIntProcessor
from uuid import UUID
import struct
class C2SLoginStartPacket(Packet):
    def __init__(self, username: str, uuid: str, protocolNumber: int, serverPort:int = 25565):
        self.username = username.encode()
        self.uuid = UUID(uuid).bytes
        self.protocolNumber = protocolNumber
        self.serverPort = serverPort
        super().__init__()
    def getBytes(self):
        self.packet = (
            VarIntProcessor.packVarInt(0x00) + 
            VarIntProcessor.packVarInt(len(self.username)) +
            self.username +
            self.uuid
        )
        return VarIntProcessor.packVarInt(len(self.packet)) + self.packet
    def getHandshake(self):
        handshake = (
            b"\x00"
            + VarIntProcessor.packVarInt(self.protocolNumber)
            + VarIntProcessor.packVarInt(len(self.username)) + self.username
            + struct.pack(">H", self.serverPort)
            + b"\x02"  # 2 login
        )
        return VarIntProcessor.packVarInt(len(handshake)) + handshake