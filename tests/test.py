from utils.version.version import MinecraftVersion, isNewer
from utils.color import Color
from mc_protocol.network.packet.varint_processor import VarIntProcessor
a = MinecraftVersion("1.21.4")
b = MinecraftVersion("1.20.5")
print(a.getMinorVersion())
print(b.getMinorVersion())
print(a.getPatchVersion())
print(isNewer(a, b))
print(VarIntProcessor.packVarInt(114514).decode("ansi"))