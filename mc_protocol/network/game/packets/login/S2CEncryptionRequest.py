from mc_protocol.network.game.packet import Packet
from mc_protocol.network.packet.varint_processor import VarIntProcessor
class S2CEncryptionRequest(Packet):
    def __init__(self, erBytes: bytes):
        self.erDict = VarIntProcessor.decodeEncryptionRequest(erBytes)

        super().__init__()
    def getServerId(self):
        return self.erDict.get("server_id")
    def getPublicKey(self):
        return self.erDict.get("public_key")
    def getVerifyToken(self):
        return self.erDict.get("verify_token")