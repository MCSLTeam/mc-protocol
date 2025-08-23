from mc_protocol.network.game.packet import Packet, ProtocolDirection, ProtocolState
from mc_protocol.network.packet.varint_processor import VarIntProcessor
class S2CEncryptionRequest(Packet):
    PACKET_ID = 0x01
    PROTOCOL_STATE = ProtocolState.LOGIN
    PROTOCOL_DIRECTION = ProtocolDirection.S2C
    def __init__(self, erBytes: bytes):
        
        er = VarIntProcessor.unpackPacket(erBytes)[2]
        offset = 0
        # 1. Server ID
        server_id_len, offset = VarIntProcessor.readVarInt(er, offset)
        server_id_end = offset + server_id_len
        server_id = er[offset:server_id_end].decode("utf-8")
        offset = server_id_end

        # 2. Public Key
        public_key_len, offset = VarIntProcessor.readVarInt(er, offset)
        public_key_end = offset + public_key_len
        public_key = er[offset:public_key_end]
        offset = public_key_end

        # 3. Verify Token
        verify_token_len, offset = VarIntProcessor.readVarInt(er, offset)
        verify_token_end = offset + verify_token_len
        verify_token = er[offset:verify_token_end]
        
        self.erDict = {
            'server_id': server_id,
            'public_key': public_key,
            'verify_token': verify_token
        }
    def getServerId(self):
        return self.erDict.get("server_id")
    def getPublicKey(self):
        return self.erDict.get("public_key")
    def getVerifyToken(self):
        return self.erDict.get("verify_token")