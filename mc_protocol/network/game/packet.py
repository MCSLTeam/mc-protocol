from abc import ABC, abstractmethod
class Packet(ABC):
    def __init__(self):
        self.packet = None
    
    def getBytes(self):
        return self.packet