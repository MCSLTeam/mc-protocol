
# 数据包基类
from abc import ABC, abstractmethod
from enum import Enum

class ProtocolState(Enum):
    HANDSHAKING = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3
class ProtocolDirection(Enum):
    C2S = "C2S"
    S2C = "S2C"

class Packet(ABC):
    PACKET_ID: int = -1
    PROTOCOL_STATE: ProtocolState | None = None
    PROTOCOL_DIRECTION: ProtocolDirection | None  = None
    def __init__(self):
        pass
    @abstractmethod
    def getPacket(self) -> bytes:
        pass
    @abstractmethod
    def getField(self) -> bytes:
        pass