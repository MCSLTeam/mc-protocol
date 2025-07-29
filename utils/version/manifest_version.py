from urllib.request import urlretrieve
from urllib.error import URLError
from os.path import join as osp_join
from json import loads
def getManifestJson(savePath: str):
    url = "https://piston-meta.mojang.com/mc/game/version_manifest.json"
    filename = url.split("/")[-1]
    path = osp_join(savePath) + filename
    try:
        content = urlretrieve(url, path)
        with open(filename, "w") as f:
            f.write(content[0])
    except:
        raise URLError(f"Error downloading {filename} from mojang offical. Please check your Internet.")
    
class ManifestVersion:
    def __init__(self, manifestPath):
        try:
            with open(manifestPath, 'r') as f:
                self.manifest: dict = loads(f.read())
        except:
            raise FileNotFoundError(f"Couldn't find manifest file {manifestPath}")
    def getLatestVersion(self):
        return self.manifest['latest']['snapshot']
    def isLatest(self, ver: str):
        return self.manifest['latest']['release'] == ver or self.manifest["latest"]['snapshot'] == ver
    
    def getVersionType(self, ver: str):
        try:
            for version in self.manifest['versions']:
                if version['id'] == ver:
                    return version['type']
        except:
            return None
     
    def getVersionUrl(self, ver: str):
        try:
            for version in self.manifest['versions']:
                if version['id'] == ver:
                    return version['url']
        except:
            return None
    def getVersionTime(self, ver: str):
        try:
            for version in self.manifest['versions']:
                if version['id'] == ver:
                    return version['time']
        except:
            return None
    def getVersionReleaseTime(self, ver: str):
        try:
            for version in self.manifest['versions']:
                if version['id'] == ver:
                    return version['releaseTime-']
        except:
            return None