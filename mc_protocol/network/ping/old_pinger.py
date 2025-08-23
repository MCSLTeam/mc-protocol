
import socket
from utils.version.version import MinecraftVersion
from exceptions.exceptions import PacketException
from mc_protocol.network.ping.pinger import Pinger

class OldPinger(Pinger):
    def __init__(self, version: MinecraftVersion | int):
        super().__init__(version)
    def ping(self) -> None:
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            sock.send(b"\xFE\x01")
            response_data = sock.recv(512)
            if not response_data.startswith(b'\xFF'):
                raise PacketException(r"Invalid packet. It doesn't start with \xFF")
            self.serverInformation = response_data[3:].decode('utf-16be').split("\x00")
    def getMotd(self) -> str:
        return self.serverInformation[3]
    def getMaxPlayers(self) -> int:
        return int(self.serverInformation[-1])
    def getOnlinePlayerNum(self) -> int:
        return int(self.serverInformation[-2])
    def getServerName(self) -> str:
        return self.serverInformation[2]
    def getServerProtocol(self) -> str:
        return self.serverInformation[2]