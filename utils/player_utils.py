import requests
from uuid import uuid3, NAMESPACE_OID, UUID
from json import loads
uuid_api = \
{
    "MOJANG-REST": "https://api.mojang.com/users/profiles/minecraft/{name}",

}
avatar_api = \
{
    "MINOTAR" : "https://minotar.net/avatar/{identifier}/{size}.png"

}
skin_api = \
{
    "MINOTAR": "https://minotar.net/skin/{identifier}"
}


class PlayerUtils:
    def __init__(self):
        pass
    @staticmethod
    def getOfflinePlayerUUID(playerID: str) -> str:
        return str(uuid3(NAMESPACE_OID, playerID))
    @staticmethod
    def getOnlinePlayerProfileByJwt(jwt: str) -> dict:
        header = {
            "Authorization": "Bearer " + jwt
        }
        response = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=header)
        response.raise_for_status()
        return loads(response.text) 
        

    @staticmethod
    def getOnlinePlayerUUIDFromMojangRest(username: str) -> str:
            url = uuid_api["MOJANG-REST"].replace("{name}", username)
            response = requests.get(url)
            response.raise_for_status()
            return str(UUID(response.json().get('id')))
    @staticmethod
    def getPlayerAvatarFromMinotar(id: str, size: int=64, savePath:str=None) -> bytes:
        """id could be name or uuid"""
        url = avatar_api['MINOTAR'].replace("{identifier}", id).replace("{size}", str(size))
        response = requests.get(url)
        response.raise_for_status()
        if savePath:
            with open(savePath if savePath.endswith(".png") else savePath + ".png", "bw") as f:
                f.write(response.content)
        return response.content
    @staticmethod
    def getPlayerSkinFromMinotar(id: str, savePath:str=None) -> bytes:
        """id could be name or uuid"""
        url = skin_api['MINOTAR'].replace("{identifier}", id)

        response = requests.get(url)
        response.raise_for_status()
        if savePath:
            with open(savePath if savePath.endswith(".png") else savePath + ".png", "bw") as f:
                f.write(response.content)
        return response.content
