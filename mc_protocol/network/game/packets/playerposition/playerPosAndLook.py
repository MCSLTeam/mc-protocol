# send:有关于玩家位置和视角的包

from packet import PacketSend
from packet import PACK_IDS
from struct import pack # 编码

class PlayerPosition(PacketSend):
    def __init__(self, x: float, y: float, z: float, yaw: float, pitch: float, onGround: bool):
        self.x = x
        self.y = y
        self.z = z
        if (yaw <= 180.0 and yaw >= -180.0) and (pitch <= 90.0 and pitch >= -90.0):
            self.yaw = yaw
            self.pitch = pitch
        else:
            self.yaw = 0
            self.pitch = 0
            print("错误的水平旋转角或垂直视角")
        self.onGround = onGround
        self.teleportID = b"\x00" # 0
        super().__init__(PACK_IDS["game"]["playerPosAndLook"], self.__getField__())

    def __getField__(self) -> bytes: # 获得字段 
        return pack(">d", self.x) + \
            pack(">d", self.y) + \
            pack(">d", self.z) + \
            pack(">d", self.yaw) + \
            pack(">d", self.pitch) + \
            b"\x01" if self.onGround else b"\x00" + \
            self.teleportID
    
    def __repr__(self):
        return f"PlayerPosition(x:{self.x}, y:{self.y}, z:{self.z}, yaw:{self.yaw}, pitch:{self.pitch}, onGround:{self.onGround})"