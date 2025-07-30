# 数据包基类
from abc import ABC, abstractmethod

PACK_IDS = {
    "status": b"\x00", # 状态查询
    "loginStart": b"\x00", # 登录
    "game": { # 游戏
        "playerPosition": b"\x18",
        "playerPosAndLook": b"\x15",
        "playerDigging": b"\x1c",
        "playerBlockPlacement": b"\x2f",
        "useItem": b"\x32",
        "interactEntity": b"\x31", # 攻击实体
        "chunkData": b"\x25" # 区块更新
    }
}

class PacketSend(ABC):
    def __init__(self, id, field: bytes): # id 和 字段
        self.id = id
        self.field = field

    def getPacket(self) -> bytes:
        return bytes(self.id) + self.field


    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __getField__(self):
        pass

class PacketAccept(ABC):
    def __init__(self, id: bytes, data: bytes): # id 和 字段
        self.id = id
        self.data = data

    @abstractmethod
    def getMsg(self):
        pass

class Packet(ABC):
    def __init__(self):
        self.packet = None
    
    def getBytes(self):
        return self.packet
