from utils.version.version import MinecraftVersion, isNewer
from utils.color import Color
from mc_protocol.network.ping.modern_pinger import ModernPinger
from mc_protocol.network.packet.varint_processor import VarIntProcessor
from mc_protocol.network.game.packets.logins.reqs import OAuth

'''p = ModernPinger(MinecraftVersion("1.8.8"))
p.setHost("127.0.0.1")
p.setPort(25565)
p.ping()
print(p.serverInformation)
# data = b'dhsauidhuaihduwhudhauihdusahdui'

# num, of = VarIntProcessor.readVarInt(data)

# print(f"num:{num}, offset:{of}")

# print(len(data))'''

print(OAuth())
