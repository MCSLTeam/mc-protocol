class MinecraftVersion:
    def __init__(self, version: str):
        self.version = version
        self.type = self.getVersion()

    def isSnapshot(self) -> bool:
        return "w" in self.version
    def isBetaVersion(self) -> bool:
        return self.version.startswith("b")
    def getVersion(self) -> str:
        return "Beta" if self.isBetaVersion() else "Snapshot" if self.isSnapshot() else "Release"
    def getMinorVersion(self) -> int:
        try:
            return int(self.version.split(".")[1])
        except IndexError:
            return int(self.version.split("w")[1])
    def getPatchVersion(self) -> int:
        try:
            return int(self.version.split(".")[2]) if type != "Snapshot" else self.version[-1]
        except IndexError:
            return 0
    def toPythonNamed(self) -> str:
        return self.version.replace(".","_")  
            
def isNewer(ver1: MinecraftVersion | str , ver2: MinecraftVersion | str):
    ver1 = MinecraftVersion(ver1) if isinstance(ver1, str) else ver1
    ver2 = MinecraftVersion(ver2) if isinstance(ver2, str) else ver2
    if ver1.type == "Snapshot" or ver2.type == "Snapshot":
        return False
    if ver1.getMinorVersion() > ver2.getMinorVersion():
        return True
    return ver1.getPatchVersion() > ver2.getPatchVersion()
    