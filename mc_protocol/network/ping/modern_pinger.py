# -*- coding:utf-8 -*-
# @author  : ZYN
# @time    : 2025-7-27
# @function: 针对于新版本(1.7)以上服务器的pinger


import socket
from json import loads
from utils.version.version import MinecraftVersion

from mc_protocol.network.ping.pinger import Pinger
from mc_protocol.network.packet.varint_processor import VarIntProcessor
class ModernPinger(Pinger):
    def __init__(self, version: int | MinecraftVersion):
        super().__init__(version)
    
    # 分块从服务器中获取数据
    # ping      
    def ping(self):
        # 建立一个套接字连接 （地址，端口） 看是否能监听到数据
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            handshake, length = VarIntProcessor.packModernServerPingHandshake(host=self.host, port=self.port, protocolNum=self.version)

            # 向服务器发送握手包
            sock.send(length)
            sock.send(handshake)
            sock.send(b"\x01\x00")
            _response = b''
            while True:
                _ = sock.recv(4096)
                _response += _
                decoded_response = _response.decode(errors="ignore")
                # 传入的包中最末尾一个字节的msb位是0，只需判断 _的最后一个元素是否就是包末尾的那个字节
                # base64有神秘字节导致循环提前结束，直接强制要有一个完整json
                if _[-1] & 0x80 == 0 and decoded_response.count("{") == decoded_response.count("}"):
                    break
    
            

            # 解析响应包    
            json_len, offset = VarIntProcessor.readVarInt(_response)
            for i in range(2):
                json_len, offset = VarIntProcessor.readVarInt(_response, offset)
            # 将解析值转为字典
            self.serverInformation = loads(_response[offset:offset+json_len].decode('utf-8', errors='ignore'))
    
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
    
        