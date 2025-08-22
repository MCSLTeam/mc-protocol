from utils.version.protocol_versions import mc_release_protocol_versions
from mc_protocol.network.game.packets.login.C2SLoginStartPacket import C2SLoginStartPacket
from mc_protocol.network.game.packets.login.S2CEncryptionRequest import S2CEncryptionRequest
from mc_protocol.network.game.packets.login.C2SEncryptionResponse import C2SEncryptionResponse
from mc_protocol.network.game.packets.login.S2CLoginSuccess import S2CLoginSuccess
from mc_protocol.network.game.packets.login.S2CSetCompression import S2CSetCompression
from mc_protocol.network.ping.modern_pinger import ModernPinger
from mc_protocol.network.ping.old_pinger import OldPinger
from utils.player_utils import PlayerUtils
from mc_protocol.network.packet.varint_processor import VarIntProcessor
from mc_protocol.network.packet.packet_encryptor import PacketEncryptor
from mc_protocol.network.oauth.oauth import oauth
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
player = oauth()
u = "096d5f34c30a4c65b60bea19b2d2a159"
pinger = ModernPinger(765)
pinger.setHost("cn-js-sq.wolfx.jp")
pinger.setPort(25566)
pinger.ping()
v = pinger.getServerProtocol()
with socket.create_connection(("cn-js-sq.wolfx.jp", 25566)) as sock:
    C2SLSP = C2SLoginStartPacket("wyh_", u, v, 25566)
    sock.send(C2SLSP.getHandshake())
    sock.send(C2SLSP.getPacket())
    
    S2CER = S2CEncryptionRequest(VarIntProcessor.readPacket(sock))
    C2SER = C2SEncryptionResponse(S2CER.getPublicKey(), S2CER.getVerifyToken())
    authWithMojang(player['access_token'], u, S2CER.getServerId(), C2SER.sharedSecret, S2CER.getPublicKey())
    sock.send(C2SER.getPacket())
    packet = VarIntProcessor.readPacket(sock)
    encryptor = PacketEncryptor(C2SER.sharedSecret)
    print(S2CSetCompression(packet, encryptor).getThreshold())
    S2CLoginSuccess(VarIntProcessor.readPacket(sock))