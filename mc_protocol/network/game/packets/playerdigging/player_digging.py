# send: 玩家挖掘方块的包
from packet import C2SPacket
from packet_ids import PACK_IDS
from packet.varint_processor import VarIntProcessor
import struct

DIG_STATUS = {
    "begin": 0,
    "cancel": 1,
    "finish": 2
}

DIG_FACES = {
    "down": "\x00",
    "up": "\x01",
    "north": "\x02",
    "south": "\x03",
    "west": "\x04",
    "east": "\x06"
}

class PlayerDigging(C2SPacket):
    def __init__(self, status: bytes, x: int, y: int, z: int, face: bytes):
        self.status = status # 挖掘状态
        self.x = x # 坐标
        self.y = y
        self.z = z
        self.face = face # 朝向
        super().__init__(PACK_IDS["game"]["playerDigging"], self.getField())

    def getField(self):
        # 这里x, y, z要放在一起压缩成长整型
        return VarIntProcessor.packVarInt(self.status) + \
            (((self.x & 0x3ffffff) << 38) | ((self.z & 0x3ffffff) << 12) | (self.y & 0xfff)).to_bytes(8, byteorder='big', signed=True) + \
            self.face
    
    def __repr__(self):
        return super().__repr__()