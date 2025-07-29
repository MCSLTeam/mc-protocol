# -*- coding:utf-8 -*-
# @author  : ZYN
# @time    : 2025-7-29
# @function: 有关于玩家位置的包

from packet import Packet
from packet import PACK_IDS
from struct import pack # 编码

class PlayerPosition(Packet):
    def __init__(self, x: float, y: float, z: float, onGround: bool):
        self.id = PACK_IDS["game"]["playerPosition"]
        self.x = x
        self.y = y
        self.z = z
        self.onGround = onGround
        super().__init__(id, self.__getField__())

    def __getField__(self) -> bytes: # 获得字段 
        return pack(">d", self.x) + \
            pack(">d", self.y) + \
            pack(">d", self.z) + \
            b"\x01" if self.onGround else b"\x00"
    
    def __repr__(self):
        return super().__repr__()