from utils.version.protocol_versions import mc_release_protocol_versions
from mc_protocol.network.game.packets.login.C2SLoginStartPacket import C2SLoginStartPacket
from mc_protocol.network.game.packets.login.S2CEncryptionRequest import S2CEncryptionRequest
from mc_protocol.network.game.packets.login.C2SEncryptionResponse import C2SEncryptionResponse
from mc_protocol.network.ping.modern_pinger import ModernPinger
from mc_protocol.network.ping.old_pinger import OldPinger
from utils.player_utils import PlayerUtils
from mc_protocol.network.game.packets.login.C2MojangSession import authWithMojang
import socket
from utils.version.version import MinecraftVersion
'''u = PlayerUtils.getOnlinePlayerUUIDFromMojangRest("pwp_ZYN")
pinger = ModernPinger(765)
pinger.setHost("cn-js-sq.wolfx.jp")
pinger.setPort(25566)
pinger.ping()
protocol = pinger.getServerProtocol()
with socket.create_connection(("cn-js-sq.wolfx.jp", 25566,), 5.0) as sock:
    lsp = C2SLoginStartPacket("pwp_ZYN", u, protocol, 25566)
    sock.send(lsp.getHandshake())
    sock.send(lsp.getPacket())
    er = sock.recv(4096)
    s2cer = S2CEncryptionRequest(er)
    c2ser= C2SEncryptionResponse(s2cer.getPublicKey(), s2cer.getVerifyToken())
    at = None
    with open("./tests/accesstoken.txt", 'r') as f:
        at = f.read()
    print(authWithMojang(at, u, '', c2ser.sharedSecret, s2cer.getPublicKey()))
    sock.send(c2ser.getPacket())
    print(c2ser.getEncryptor().deEncryptPacket(sock.recv(4096)))'''
version = MinecraftVersion("1.8.8")
pinger = ModernPinger(version)
pinger.setHost("127.0.0.1")
pinger.setPort(25565)
pinger.ping()
with socket.create_connection(("127.0.0.1", 25565), 5.0) as s:
    startPack = C2SLoginStartPacket("nihao", PlayerUtils.getOfflinePlayerUUID("nihao"), mc_release_protocol_versions["1.8.8"])
    s.send(startPack.getHandshake())
    s.send(startPack.getPacket())


