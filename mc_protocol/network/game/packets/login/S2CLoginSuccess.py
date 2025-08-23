from mc_protocol.network.game.packet import Packet, ProtocolDirection, ProtocolState
from mc_protocol.network.packet.varint_processor import VarIntProcessor
class S2CLoginSuccess(Packet):
    PACKET_ID = 0x02
    PROTOCOL_STATE = ProtocolState.LOGIN
    PROTOCOL_DIRECTION = ProtocolDirection.S2C
    def __init__(self, packet, encryptor):
        self.encryptor = encryptor
        packet = encryptor.deEncryptPacket(packet)
        plength, packetid, encrypted_content = VarIntProcessor.unpackPacket(packet)

        print(f"加密包总长度: {plength}")
        print(f"包ID: {packetid} (0x{packetid:02X})")
        print(f"加密内容长度: {len(encrypted_content)}")
        print(f"加密内容: {encrypted_content.hex()}")
        decrypted_content = encryptor.deEncryptPacket(encrypted_content)

        print(f"解密后内容: {decrypted_content.hex()}")
        print(f"解密后文本: {decrypted_content}")
