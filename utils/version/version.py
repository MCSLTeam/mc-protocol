# -*- coding:utf-8 -*-
# @author  : Yurnu
# @time    : 2025-7-27
# @function: 对MC版本进行处理，加以归类，判断


from utils.version.protocol_versions import mc_release_protocol_versions
class MinecraftVersion:
    def __init__(self, version: str):
        self.version = version
        self.type = self.getVersionType()
    
    def isSnapshot(self) -> bool: # 判断是否是快照版本 21w19a之类的
        return "w" in self.version or "rc" in self.version or "pre" in self.version
    def isBetaVersion(self) -> bool: # 判断是否是beta版
        return self.version.startswith("b")
    def getVersionType(self) -> str: # 获得版本的类型
        return "Beta" if self.isBetaVersion() else "Snapshot" if self.isSnapshot() else "Release"
    def getMainVersion(self) -> int:
        return int(self.version.split("w")[0]) if self.type =="Snapshot" else 1
    def getMinorVersion(self) -> int: # 获得二级版本号
        try:
            return int(self.version.split(".")[1])
        except IndexError: # 21w19a
            return int(self.version.split("w")[1])
    def getPatchVersion(self) -> int: # 获得三级版本号
        try: # 如果是 1.12.2 的话就获取最后一个元素
            return int(self.version.split(".")[2]) if self.type != "Snapshot" else self.version[-1]
        except IndexError: # 如果没有第三级，就返回0
            return 0
    def toPythonNamed(self) -> str:
        return self.version.replace(".","_")  
    
    def getReleaseProtocolVersion(self) -> int:
        return mc_release_protocol_versions[self.version]
def isNewer(ver1: MinecraftVersion | str , ver2: MinecraftVersion | str):
    ver1 = MinecraftVersion(ver1) if isinstance(ver1, str) else ver1
    ver2 = MinecraftVersion(ver2) if isinstance(ver2, str) else ver2

    return ver1.getMainVersion() > ver2.getMainVersion() or ver1.getMinorVersion() > ver2.getMinorVersion() or ver1.getPatchVersion() > ver2.getPatchVersion()
