import socket
from io import BytesIO
import zlib

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
    def readPacket(sock: socket.socket) -> bytes:
        varint_bytes = bytearray()
        for i in range(5):
            byte = sock.recv(1)
            if not byte:
                raise ConnectionError("Connection closed while trying to read packet length.")
            
            varint_bytes.append(byte[0])
            if (byte[0] & 0x80) == 0:
                break
        else:
            raise ValueError("Invalid VarInt packet received.")
        packet_data_length, _ = VarIntProcessor.readVarInt(varint_bytes)
        del _
        data_buffer = bytearray()
        bytes_to_read = packet_data_length
        while len(data_buffer) < bytes_to_read:
            remaining_bytes = bytes_to_read - len(data_buffer)
            chunk = sock.recv(remaining_bytes)
            
            if not chunk:
                raise ConnectionError("Connection closed unexpectedly while reading packet data.")
            
            data_buffer.extend(chunk)
        return bytes(varint_bytes) + bytes(data_buffer)
    @staticmethod
    def unpackPacket(packet: bytes) -> tuple[int, int, bytes]:
        offset = 0
        packetLength, offset = VarIntProcessor.readVarInt(packet, offset)

        packet_id, offset = VarIntProcessor.readVarInt(packet, offset)
    
        packet_content = packet[offset:]
        del offset
        return (packetLength, packet_id, packet_content)
    @staticmethod
    def unpackCompressedPacket(packet: bytes) -> tuple[int, int, int, bytes]:
        offset = 0
        packet_length, offset = VarIntProcessor.readVarInt(packet, offset)
        
        data_length, offset = VarIntProcessor.readVarInt(packet, offset)
        
        remaining_data = packet[offset:]

        if data_length == 0:
            uncompressed_data = remaining_data
        else:
            uncompressed_data = zlib.decompress(remaining_data)
            if len(uncompressed_data) != data_length:
                raise ValueError(
                    f"Expected {data_length} bytes, got {len(uncompressed_data)}"
                )
        id_offset = 0
        packet_id, id_offset = VarIntProcessor.readVarInt(uncompressed_data, id_offset)
        payload = uncompressed_data[id_offset:]

        return (packet_length, data_length, packet_id, payload)