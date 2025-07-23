import socket

from mc_protocol.network.ping.pinger import Pinger
class ModernPinger(Pinger):
    def __init__(self):
        self.host = None
        self.port = None
    def getMotd():
        with socket