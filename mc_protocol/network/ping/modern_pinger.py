import socket
from json import loads
from utils.version.version import MinecraftVersion

from mc_protocol.network.ping.pinger import Pinger
from mc_protocol.network.packet.varint_processor import VarIntProcessor
class ModernPinger(Pinger):
    def __init__(self, version: int | MinecraftVersion):
        super().__init__(version)
    def ping(self):
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            handshake, length = VarIntProcessor.packModernServerPingHandshake(host=self.host, port=self.port, protocolNum=self.version)

            sock.send(length)
            sock.send(handshake)
            sock.send(b"\x01\x00")
            
            _response = b''
            while True:
                _ = sock.recv(4096)
                if not _:
                    break
                _response += _
                try:
                    length, offset = VarIntProcessor.readVarInt(_response)
                    if len(_response) >= offset + length:
                        break
                except:
                    continue
                
            json_len, offset = VarIntProcessor.readVarInt(_response)
            for i in range(2):
                json_len, offset = VarIntProcessor.readVarInt(_response, offset)

            self.serverInformation = loads(_response[offset:offset+json_len].decode('utf-8', errors='ignore'))
        return True
    def getMotd(self):
        return self.serverInformation['description']['text'] if self.serverInformation else None
    def getMaxPlayers(self):
        return self.serverInformation['players']['max'] if self.serverInformation else None
    def getOnlinePlayerNum(self):
        return self.serverInformation['players']['online'] if self.serverInformation else None
    def getServerName(self):
        return self.serverInformation['version']['name'] if self.serverInformation else None
    def getServerProtocol(self):
        return self.serverInformation['version']['protocol'] if self.serverInformation else None
    
        