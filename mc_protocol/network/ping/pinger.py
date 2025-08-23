# -*- coding:utf-8 -*-
# @author  : Yurnu
# @time    : 2025-7-27
# @function: pinger基类


from abc import ABC, abstractmethod
from utils.version.version import MinecraftVersion
class Pinger(ABC):
    def __init__(self, version: int | MinecraftVersion):
        self.host = None # 服务器地址
        self.port = None # 服务器端口号
        self.timeout = 5.0 # 设置响应时间限度
        self.version = version if isinstance(version, int) else version.getReleaseProtocolVersion() # 服务器对应的MC版本
        self.serverInformation: dict = None # 服务器信息字典
    
    # host
    def setHost(self, host: str) -> None:
        self.host = host
    
    # port
    def setPort(self, port: int) -> None:
        self.port = port
    
    #获得服务器的相关信息
    
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