import socket

from utils.version.version import MinecraftVersion
from mc_protocol.network.ping.pinger import Pinger
class ModernPinger(Pinger):
    def __init__(self, version: int | MinecraftVersion):
        super().__init__(version)
    def getMotd():
        