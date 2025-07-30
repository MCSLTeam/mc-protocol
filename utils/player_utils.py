from uuid import uuid3, NAMESPACE_OID, UUID
import requests
uuid_api = \
{
    "MOJANG-REST": "https://api.mojang.com/users/profiles/minecraft/{name}",

}
avatar_api = \
{
    "MINOTAR" : "https://minotar.net/avatar/{identifier}/{size}.png"

}


class PlayerUtils:
    def __init__(self):
        pass
    @staticmethod
    def getOfflinePlayerUUID(playerID: str):
        return uuid3(NAMESPACE_OID, playerID)
    @staticmethod
    def getOnlinePlayerUUIDFromMojangRest(username: str):
        try:
            
            url = uuid_api["MOJANG-REST"].replace("{name}", username)
            response = requests.get(url)
            if response.status_code != 200: return None
            return str(UUID(response.json().get('id')))
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def getPlayerAvatarFromMinotar(id: str, size: int=64, savePath:str=None):
        """id could be name or uuid"""
        url = avatar_api['MINOTAR'].replace("{identifier}", id).replace("{size}", str(size))
        try:
            response = requests.get(url)
            if savePath:
                with open(savePath if savePath.endswith(".png") else savePath + ".png", "bw") as f:
                    f.write(response.content)
            return response.content if response.status_code == 200 else response.status_code
        except Exception as e:
            print(e)
            return None

