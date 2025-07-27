from urllib.request import urlretrieve



def GetManifest(url: str, dir: str): 
    filename = url.split("/")[-1]
    path = dir + "/" + filename
    urlretrieve(url, path)
    return open(path, "r").read()

print(GetManifest("https://piston-meta.mojang.com/mc/game/version_manifest.json", "."))

