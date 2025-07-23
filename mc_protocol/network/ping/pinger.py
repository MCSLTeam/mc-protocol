from abc import ABC, abstractmethod
class Pinger(ABC):
    def __init__(self):
        self.host = None
        self.port = None
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