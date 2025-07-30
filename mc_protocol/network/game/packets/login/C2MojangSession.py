import requests
from hashlib import sha1
from uuid import UUID
def authWithMojang(accessToken: str, uuid: str, server_id: str, sharedSecret: bytes, publicKey: bytes) -> bool:
    hasher = sha1()
    hasher.update(server_id.encode('latin-1'))
    hasher.update(sharedSecret)
    hasher.update(publicKey)
    num = int.from_bytes(hasher.digest(), byteorder='big', signed=True)
    
    if num < 0:
        hash = '-' + hex(abs(num))[2:]
    else:
        hash = hex(num)[2:]
    url = "https://sessionserver.mojang.com/session/minecraft/join"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "accessToken": accessToken,
        "selectedProfile": UUID(uuid).hex,  # 确保UUID不带破折号
        "serverId": hash
    }
    response: requests.Response = None
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 204:
        return True
    else:
        response.raise_for_status()
        return False
        
        


    