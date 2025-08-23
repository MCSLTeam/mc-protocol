import socket
from io import BytesIO

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
        # 利用Buffer缓冲区来读取varint,郝处:能动态更新buffer指针的值
    def readVarintFromBuffer(buffer: BytesIO) -> int:
        sum = 0
        shift = 0
        while True:
            byte = buffer.read(1) 
            sum |= (byte[0] & 0b01111111) << shift
            shift += 7
            if (byte[0] & 0b10000000) == 0:
                return sum
        
    @staticmethod
    def readPacket(sock: socket) -> bytes:
        packet = bytearray()
        packetLength = None
        varintLength = 0
        
        while True:
            if packetLength is not None and len(packet) >= packetLength + varintLength:
                break

            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError("Connection closed")
            packet.extend(chunk)
            if packetLength is None:
                packetLength, varintLength = VarIntProcessor.readVarInt(packet)
        return bytes(packet)
    @staticmethod
    def unpackPacket(packet: bytes) -> tuple[int, int, bytes]:
        offset = 0
        packetLength, offset = VarIntProcessor.readVarInt(packet, offset)

        packet_id, offset = VarIntProcessor.readVarInt(packet, offset)
    
        packet_content = packet[offset:]
        del offset
        return (packetLength, packet_id, packet_content)
        