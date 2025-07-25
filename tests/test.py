from utils.version.version import MinecraftVersion, isNewer
from utils.color import Color
from mc_protocol.network.ping.modern_pinger import ModernPinger
from mc_protocol.network.ping.old_pinger import OldPinger
a = MinecraftVersion("1.21.4")
b = MinecraftVersion("1.20.5")
print(a.getMinorVersion())
print(b.getMinorVersion())
print(a.getPatchVersion())
print(isNewer(a, b))
pinger = OldPinger(a)
pinger.setHost("cn-js-sq.wolfx.jp")
pinger.setPort(25566)

pinger.ping()
#print(pinger.serverInformation)
print(pinger.getMotd())
print(pinger.getServerName())
print(pinger.getServerProtocol())
print(pinger.getOnlinePlayerNum())