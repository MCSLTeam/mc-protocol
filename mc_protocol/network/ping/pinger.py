from abc import ABC, abstractmethod
from utils.version.version import MinecraftVersion
class Pinger(ABC):
    def __init__(self, version: int | MinecraftVersion):
        self.host = None
        self.port = None
        self.timeout = 5.0
        self.version = version if isinstance(version, int) else version.getReleaseProtocolVersion()
        self.serverInformation: dict | list = None
    def setHost(self, host: str):
        self.host = host
    def setPort(self, port: int):
        self.port = port
    def setTimeout(self, timeout:float):
        self.timeout = timeout
        
    @abstractmethod
    def getMotd(self) -> str:
        pass
    @abstractmethod
    def getOnlinePlayerNum(self) -> int:
        pass
    @abstractmethod
    def getMaxPlayers(self) -> int:
        pass
    @abstractmethod
    def getServerName(self) -> str:
        pass
    @abstractmethod
    def getServerProtocol(self) -> int | str:
        pass
    @abstractmethod
    def ping(self):
        pass