
# 数据包基类
from abc import ABC, abstractmethod


class C2SPacket(ABC):
    def __init__(self, id): # id 和 字段
        self.id = id
        self.field = self.getField()
    @abstractmethod
    def getPacket(self) -> bytes:
        pass
    @abstractmethod
    def getField(self) -> bytes:
        pass
    def getId(self):
        return self.id
class S2CPacket(ABC):
    def __init__(self):
        pass
