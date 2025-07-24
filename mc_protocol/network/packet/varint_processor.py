class VarIntProcessor:
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
    def readVarInt(data: bytes, offset:int = 0):
        result = 0
        while True:
            byte = data[offset]
            byte = byte & 0x7F # 0b01111111 因为varint取低7位
            byte <<= offset
            offset += 7 # 下一个7位
            result += byte
            if (byte & 0x80) == 0:  # varint规定，当高1位为0时包结束
                break
        return result



