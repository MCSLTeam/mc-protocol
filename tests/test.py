from utils.version.version import MinecraftVersion, isNewer
from utils.player_utils import PlayerUtils
from utils.color import Color
from mc_protocol.network.ping.modern_pinger import ModernPinger
from mc_protocol.network.packet.varint_processor import VarIntProcessor
<<<<<<< HEAD


p = ModernPinger(MinecraftVersion("1.8.8"))
p.setHost("127.0.0.1")
p.setPort(25565)
p.ping()
print(p.serverInformation)
# data = b'dhsauidhuaihduwhudhauihdusahdui'

# num, of = VarIntProcessor.readVarInt(data)

# print(f"num:{num}, offset:{of}")

# print(len(data))


=======
from mc_protocol.network.game.packets.login.C2SLoginStartPacket import C2SLoginStartPacket
from mc_protocol.network.game.packets.login.S2CEncryptionRequest import S2CEncryptionRequest
from mc_protocol.network.game.packets.login.C2SEncryptionResponse import C2SEncryptionResponse
import socket
u = PlayerUtils.getOnlinePlayerUUIDFromMojangRest("wyh_")
pinger = ModernPinger(765)
pinger.setHost("cn-js-sq.wolfx.jp")
pinger.setPort(25566)
pinger.ping()
protocol = pinger.getServerProtocol()
with socket.create_connection(("cn-js-sq.wolfx.jp", 25566,), 5.0) as sock:
    lsp = C2SLoginStartPacket("wyh_", u, protocol, 25566)
    sock.send(lsp.getHandshake())
    sock.send(lsp.getBytes())
    er = sock.recv(4096)
    s2cer = S2CEncryptionRequest(er)
    c2ser= C2SEncryptionResponse(s2cer.getPublicKey(), s2cer.getVerifyToken())
    sock.send(c2ser.getBytes())
    print(c2ser.getEncryptor().deEncryptPacket(sock.recv(4096)))
    
>>>>>>> origin/main
