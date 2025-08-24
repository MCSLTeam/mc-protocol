from mc_protocol.network.game.packet import Packet, ProtocolDirection, ProtocolState
from mc_protocol.network.packet.varint_processor import VarIntProcessor
from mc_protocol.network.packet.packet_encryptor import PacketEncryptor
from os import urandom
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
class C2SEncryptionResponse(Packet):
    PACKET_ID = 0x00
    PROTOCOL_STATE = ProtocolState.LOGIN
    PROTOCOL_DIRECTION = ProtocolDirection.C2S
    def __init__(self, publicKey: bytes, verifyToken: bytes):
        self.publicKey = publicKey
        self.verifyToken = verifyToken
        self.sharedSecret = urandom(16)
    
    def getField(self):

        publicKey = RSA.import_key(self.publicKey)
        cipher = PKCS1_v1_5.new(publicKey)

        e_sharedSecret = cipher.encrypt(self.sharedSecret)
        e_verifyToken = cipher.encrypt(self.verifyToken)
        del cipher
        field = (
            
            VarIntProcessor.packVarInt(len(e_sharedSecret)) +
            e_sharedSecret +
            VarIntProcessor.packVarInt(len(e_verifyToken)) +
            e_verifyToken
            )
            
        return field
    def getPacket(self):
        _ = VarIntProcessor.packVarInt(0x01) + self.getField()
        return VarIntProcessor.packVarInt(len(_)) + _
    def getEncryptor(self):
        return PacketEncryptor(self.sharedSecret)