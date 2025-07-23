from utils.version.version import MinecraftVersion, isNewer
from utils.color import Color
from mc_protocol.network.ping.ping import getPinger
a = MinecraftVersion("1.21.4")
b = MinecraftVersion("1.20.5")
print(a.getMinorVersion())
print(b.getMinorVersion())
print(a.getPatchVersion())
print(isNewer(a, b))
pinger = getPinger(MinecraftVersion("1.5"))
pinger.setHost("2b2t.xin")
pinger.setPort(25565)
c = pinger.getMotd()
print(c)
print(Color.textToANSICoded(c))

print(pinger.getMaxPlayers())