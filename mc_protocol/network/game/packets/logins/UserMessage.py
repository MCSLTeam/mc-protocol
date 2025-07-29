# -*- coding:utf-8 -*-
# @author  : ZYN
# @time    : 2025-7-29
# @function: 初始化玩家数据
import uuid


class User():
    def __init__(self, msg: dict | str):
        # 正版用户的字典 （通过网络请求获得）
        if isinstance(msg, dict):
            try: 
                self.username = msg.username 
                self.accessToken = msg.accessToken # 用户通行码
                self.uuid = msg.uuid # uuid 
                self.type = "msa" # 微软用户
            except:
                print("用户信息不完整或错误")
        # 离线用户
        else:
            self.username = msg
            self.accessToken = "{}"
            self.type = "Legacy" # 离线用户
            self.uuid = uuid.uuid1() # 基于时间戳生成随机uuid    

    # 获得用户各种信息
    def getUsername(self):
        return self.username
    def getAccessToken(self):
        return self.accessToken
    def getUUID(self):
        return self.uuid
    def getType(self):
        return self.type