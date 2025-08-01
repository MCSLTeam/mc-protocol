# -*- coding:utf-8 -*-
# @author  : ZYN
# @time    : 2025-7-27
# @function: 针对于新版本(1.7)以上服务器的pinger


import socket
from struct import pack
from json import loads
from utils.version.version import MinecraftVersion
from io import BytesIO
from mc_protocol.network.ping.pinger import Pinger
from mc_protocol.network.packet.varint_processor import VarIntProcessor
class ModernPinger(Pinger):
    def __init__(self, version: int | MinecraftVersion):
        super().__init__(version)
    

    # ping      
    def ping(self):
        # 建立一个套接字连接 （地址，端口） 看是否能监听到数据
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            handshake = (
            b"\x00" +
            VarIntProcessor.packVarInt(self.version) +
            VarIntProcessor.packVarInt(len(self.host)) +  
            self.host.encode() +
            pack(">H", self.port) +
            b'\x01'
        )
            length = VarIntProcessor.packVarInt(len(handshake))
    

            # 向服务器发送握手包
            sock.send(length)
            sock.send(handshake)
            sock.send(b"\x01\x00")
            _response = b''
            try:
                _response = VarIntProcessor.readPacket(sock)
                (packetLength, packet_id, packet_content) = VarIntProcessor.unpackPacket(_response)
                buffer = BytesIO(packet_content)
                jsonLen = VarIntProcessor.readVarintFromBuffer(buffer)
                json = buffer.read(jsonLen)
                self.serverInformation = loads(json.decode('utf-8', errors='ignore'))
            except ConnectionError:
                print("")
            '''# 解析响应包    
            json_len, offset = VarIntProcessor.readVarInt(_response)
            for i in range(2):
                json_len, offset = VarIntProcessor.readVarInt(_response, offset)
            # 将解析值转为字典
            self.serverInformation = loads(_response[offset:offset+json_len].decode('utf-8', errors='ignore'))
            print(self.serverInformation)'''
            
    
    # 获得服务器motd
    def getMotd(self):
        return self.serverInformation['description']['text'] if self.serverInformation else None
    
    # 获得最大玩家数量
    def getMaxPlayers(self):
        return self.serverInformation['players']['max'] if self.serverInformation else None
    
    # 获得在线玩家数量
    def getOnlinePlayerNum(self):
        return self.serverInformation['players']['online'] if self.serverInformation else None
    
    # 获得服务器名字
    def getServerName(self):
        return self.serverInformation['version']['name'] if self.serverInformation else None
    
    # 获得协议码
    def getServerProtocol(self):
        return self.serverInformation['version']['protocol'] if self.serverInformation else None
    
        