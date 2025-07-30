
from mc_protocol.network.game.packets.login.C2SLoginStartPacket import C2SLoginStartPacket
from mc_protocol.network.game.packets.login.S2CEncryptionRequest import S2CEncryptionRequest
from mc_protocol.network.game.packets.login.C2SEncryptionResponse import C2SEncryptionResponse
from mc_protocol.network.ping.modern_pinger import ModernPinger
from utils.player_utils import PlayerUtils
from mc_protocol.network.game.packets.login.C2MojangSession import authWithMojang
import socket
u = PlayerUtils.getOnlinePlayerUUIDFromMojangRest("pwp_ZYN")
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
    print(authWithMojang("eyJraWQiOiIwNDkxODEiLCJhbGciOiJSUzI1NiJ9.eyJ4dWlkIjoiMjUzNTQyNTg1NTMxMjUyNCIsImFnZyI6IkFkdWx0Iiwic3ViIjoiOGViMzIwYmYtZjViNi00MTg3LWJkNmQtNTExODUzOTcwMmM4IiwiYXV0aCI6IlhCT1giLCJucyI6ImRlZmF1bHQiLCJyb2xlcyI6W10sImlzcyI6ImF1dGhlbnRpY2F0aW9uIiwiZmxhZ3MiOlsib3JkZXJzXzIwMjIiLCJtc2FtaWdyYXRpb25fc3RhZ2U0IiwidHdvZmFjdG9yYXV0aCIsIm11bHRpcGxheWVyIl0sInByb2ZpbGVzIjp7Im1jIjoiZjJkMTEyZjQtMWUwOC00MzA0LTkzYTgtYWZiMDIzMmQ4NTJhIn0sInBsYXRmb3JtIjoiUENfTEFVTkNIRVIiLCJwZmQiOlt7InR5cGUiOiJtYyIsImlkIjoiZjJkMTEyZjQtMWUwOC00MzA0LTkzYTgtYWZiMDIzMmQ4NTJhIiwibmFtZSI6InB3cF9aWU4ifV0sIm5iZiI6MTc1Mzg3ODIxNSwiZXhwIjoxNzUzOTY0NjE1LCJpYXQiOjE3NTM4NzgyMTV9.fU-Kb_CrhiUyZXyUqIr6HWEIUBuXPZLgTkyGKxIlMoN4r2L_M9REglT2B2IiiRfmYTO2Fm4OqUKJ1Bu5qYdbGtJNi3RxzqVg-hhCuGe9oueSnKnUteJlJwUj2qLDxGm3Yqzq-Lftqvs5TjmTt_eut1CEBglpYa-E3lpPmKeOim9XQltSp1QSukzZCNQ0nXr7vT99YzUpsmNHE8LwW2d3gKocGymXXz67yx3YMVGsxiCYtrPY0oUZgwozWJAnt__SiuSztqQcu-oO8pv3NpYwkUovjwcAKNVJoVefxoVXrBkDW1ANpkK203HIab6wQZoH2x057Nh9rq1xrSi1YAT20g", u, '', c2ser.sharedSecret, s2cer.getPublicKey()))
    print(c2ser.getEncryptor().deEncryptPacket(sock.recv(4096)))
