from webbrowser import open as webOpen
from requests import post, get
from mc_protocol.network.oauth.redirect_server import CodeServer, CodeHandler
from requests import get
from json import loads, dumps



def oauth():
    # 创建服务器实例
    server = CodeServer(('', 11451), CodeHandler)
       
    code = ""
    webOpen("https://login.live.com/oauth20_authorize.srf\
    ?client_id=18a1a4c2-ccae-4306-9e55-e9500a1793d7\
    &response_type=code\
    &scope=XboxLive.signin offline_access\
    &redirect_uri=http://localhost:11451/")
    server.serve_forever()
    server.server_close()
    
    '''if exists("./codeFile.txt"):
        file = open("./codeFile.txt", "r")
        if file.read() != "":
            code = file.read()'''

    code = CodeHandler.code    
    print(code)

    data = {
        "client_id": "18a1a4c2-ccae-4306-9e55-e9500a1793d7",
        "code": code, 
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:11451",
        "scope": "XboxLive.signin offline_access"
    }
    url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = post(url=url, data=data, headers=header)
    print(res)
    dic = loads(res.text)
    access_token = dic["access_token"]

    

    # XBox Live 身份验证
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": access_token # 第二步中获取的访问令牌
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    url = "https://user.auth.xboxlive.com/user/authenticate"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = dumps(data)
    res = post(url=url, data=data, headers=header)
    Token = loads(res.text)["Token"]
    uhs = str()
    for i in loads(res.text)["DisplayClaims"]["xui"]:
        uhs = i["uhs"]
    '''

    XSTS 身份验证

    '''
    data = dumps({
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [
                Token
            ]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    })
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    res = post(url=url, data=data, headers=header)
    dic = loads(res.text)
    XSTS_token = dic["Token"]
    '''

    获取 Minecraft 访问令牌

    ''' 
    data = dumps({
        "identityToken": "XBL3.0 x=" + uhs + ";" + XSTS_token
    })
    url = "https://api.minecraftservices.com/authentication/login_with_xbox"
    res = post(url=url, data=data)
    dic = loads(res.text)
    jwt = dic["access_token"]#jwt token,也就是Minecraft访问令牌

    header = {
        "Authorization": "Bearer " + jwt
    }
    res = get(url = "https://api.minecraftservices.com/entitlements/mcstore", headers=header)
    if(res.text == ""):
        return {}
    else:
        '''
        
        获取玩家 UUID
        
        '''
        header = {
            "Authorization": "Bearer " + jwt
        }
        res = get(url="https://api.minecraftservices.com/minecraft/profile", headers=header)
        dic = loads(res.text)
        username = dic["name"]#用户名
        uuid = dic["id"]#uuid

        return {
            "username": username,
            "uuid": uuid,
            "access_token": jwt
        }
        
    