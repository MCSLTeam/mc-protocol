from webbrowser import open as webOpen
from requests import post, get
from mc_protocol.network.oauth.redirect_server import CodeServer, CodeHandler
from json import loads, dumps
from utils.player_utils import PlayerUtils


def oauth() -> dict[str, str]:
    # 创建服务器实例
    server = CodeServer(('', 11451), CodeHandler)
       
    code = ""
    webOpen("https://login.live.com/oauth20_authorize.srf\
    ?client_id=18a1a4c2-ccae-4306-9e55-e9500a1793d7\
    &response_type=code\
    &scope=XboxLive.signin offline_access\
    &redirect_uri=http://localhost:11451")
    server.handle_request()
    server.server_close()
    
    '''if exists("./codeFile.txt"):
        file = open("./codeFile.txt", "r")
        if file.read() != "":
            code = file.read()'''

    code = CodeHandler.code    

    data = {
        "client_id": "18a1a4c2-ccae-4306-9e55-e9500a1793d7",
        "code": code, 
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:11451",
        "scope": "XboxLive.signin offline_access",
        "client_secret": ".1p8Q~pZg4SAtJbRckX2Iq-TW8V3_sWkd-h7maQA"
    }
    url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = post(url=url, data=data, headers=header)
    result = loads(res.text)
    access_token = result["access_token"]

    

    # XBox Live 身份验证
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={access_token}" # 第二步中获取的访问令牌
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    url = "https://user.auth.xboxlive.com/user/authenticate"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    res = post(url=url, json=data, headers=header)
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
    result = loads(res.text)
    XSTS_token = result["Token"]
    '''

    获取 Minecraft 访问令牌

    ''' 
    data = dumps({
        "identityToken": "XBL3.0 x=" + uhs + ";" + XSTS_token
    })
    url = "https://api.minecraftservices.com/authentication/login_with_xbox"
    res = post(url=url, data=data)
    result = loads(res.text)
    jwt = result["access_token"]#jwt token,也就是Minecraft访问令牌

    header = {
        "Authorization": "Bearer " + jwt
    }
    res = get(url = "https://api.minecraftservices.com/entitlements/mcstore", headers=header)
    if(res.text == ""):
        return {}  # 玩家没有购买mc
    else:
        result = PlayerUtils.getOnlinePlayerProfileByJwt(jwt)
        username = result["name"]#用户名
        uuid = result["id"]#uuid
        return {
            "username": username,
            "uuid": uuid,
            "microsoft_token": access_token,
            "access_token": jwt,
            "xsts_token": XSTS_token

        }
        
    