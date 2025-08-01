from struct import pack
import socket
class VarIntProcessor:
    # 遵循算法:varint  参考博客:https://blog.csdn.net/weixin_43708622/article/details/111397322
    @staticmethod
    def packVarInt(value: int) -> bytes:
        buf = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            buf.append(byte | (0x80 if value > 0 else 0))
            if value == 0:
                break
        return bytes(buf)
    @staticmethod
    def readVarInt(data: bytes, offset: int = 0) -> tuple[int, int]:
        result = 0
        shift = 0
        while True:
            if offset >= len(data):
                raise ValueError("Invalid VarInt packet.")
            byte = data[offset]
            offset += 1
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
            if shift >= 28:
                raise ValueError("VarInt too large")
        return result, offset
    @staticmethod
    def readPacket(self, sock: socket) -> bytes:
        buffer = bytearray()
        packetLength = None
        varintLength = 0
        
        while True:
            if packetLength is not None and len(buffer) >= packetLength + varintLength:
                break

            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError("Connection closed")
            buffer.extend(chunk)
            if packetLength is None:
                packetLength, varintLength = self.readVarInt(buffer)
        return bytes(buffer)
    @staticmethod
    def unpackPacket(packet: bytes):
        offset = 0
        packetLength, offset = VarIntProcessor.readVarInt(packet, offset)

        packet_id, offset = VarIntProcessor.readVarInt(packet, offset)
    
        packet_content = packet[offset:]
        del offset
        return (packetLength, packet_id, packet_content)
    @staticmethod
    def decodeEncryptionRequest(er: bytes) -> dict:
        er = VarIntProcessor.unpackPacket(er)[2]
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

        # 3. verify token
        verify_token_len, offset = VarIntProcessor.readVarInt(er, offset)
        verify_token_end = offset + verify_token_len
        verify_token = er[offset:verify_token_end]
        
        return {
            'server_id': server_id,
            'public_key': public_key,
            'verify_token': verify_token
        }
