from uuid import uuid3, NAMESPACE_OID, UUID
import requests
uuid_api = \
{
"MOJANG-REST": "https://api.mojang.com/users/profiles/minecraft/{name}",
"MINOTAR-REVERSE": "https://minotar.net/avatar/{name}/2.png"


}


class PlayerUtils:
    def __init__(self):
        pass
    @staticmethod
    def getOfflinePlayerUUID(playerID: str):
        return uuid3(NAMESPACE_OID, playerID)
    @staticmethod
    def getOnlinePlayerUUID(username: str, api: str="MOJANG-REST"):
        if api.upper() not in list(uuid_api.keys()):
            raise ValueError(f"Unknown api {api}")
        try:
            
            url = uuid_api[api].replace("{name}", username)

            if api == "MOJANG-REST":
                response = requests.get(url)
                if response.status_code != 200: return None
                return str(UUID(response.json().get('id')))
        except Exception as e:
            print(e)
            return None
    @staticmethod
    async def getOnlinePlayerUUID(username: str, api: str="MOJANG-REST"):
        if api.upper() not in list(uuid_api.keys()):
            raise ValueError(f"Unknown api {api}")
        try:
            
            url = uuid_api[api].replace("{name}", username)

            if api == "MOJANG-REST":
                response = await requests.get(url)
                if response.status_code != 200: return None
                return str(UUID(response.json().get('id')))
        except Exception as e:
            print(e)
            return None