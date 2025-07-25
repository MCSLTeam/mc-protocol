class PacketException(Exception):
    def __init__(self, text):
        super().__init__(text)

class VarIntException(Exception):
    def __init__(self, text):
        super().__init__(text)