from abc import ABC, abstractmethod
from utils.version.version import MinecraftVersion
class Pinger(ABC):
    def __init__(self, version: int | MinecraftVersion):
        self.host = None
        self.port = None
        self.version = version if isinstance(version, int) else version.getReleaseProtocolVersion
    def setHost(self, host: str):
        self.host = host
    def setPort(self, port: int):
        self.port = port
    @abstractmethod
    def getMotd(self) -> str:
        pass
    @abstractmethod
    def getOnlinePlayers(self) -> int:
        pass
    @abstractmethod
    def getMaxPlayers(self) -> int:
        pass