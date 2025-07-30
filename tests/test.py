
'''from mc_protocol.network.game.packets.login.C2SLoginStartPacket import C2SLoginStartPacket
from mc_protocol.network.game.packets.login.S2CEncryptionRequest import S2CEncryptionRequest
from mc_protocol.network.game.packets.login.C2SEncryptionResponse import C2SEncryptionResponse
from mc_protocol.network.ping.modern_pinger import ModernPinger
from utils.player_utils import PlayerUtils
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
    sock.send(lsp.getPacket())
    er = sock.recv(4096)
    s2cer = S2CEncryptionRequest(er)
    c2ser= C2SEncryptionResponse(s2cer.getPublicKey(), s2cer.getVerifyToken())
    sock.send(c2ser.getPacket())
    print(c2ser.getEncryptor().deEncryptPacket(sock.recv(4096)))'''


from mc_protocol.network.oauth.oauth import oauth

oauth()



