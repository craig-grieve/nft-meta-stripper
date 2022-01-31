import requests
import json


class NFTMetaStripper:
    meta = {}
    META_LINK = ""
    QUANTITY = 1


    def __init__(self, metaId, quantity=1):
        self.META_LINK = self._convertIpfsLink(metaId=metaId)
        self.QUANTITY = quantity


    def _convertImgAddress(self, metaImageString):
        # Converts the meta address into the web address for the meta image
        return "https://ipfs.io/ipfs/{}".format(metaImageString[7:])


    def _convertIpfsLink(self, metaId):
        return "https://ipfs.io/ipfs/{}".format(metaId)


    def fetchSingleMeta(self, number):
        r = requests.get("{}/{}".format(self.META_LINK, str(number)))

        jsn = json.loads(r.text)

        img = self._convertImgAddress(metaImageString=jsn["image"])

        output = {
            "image": img,
            "name": jsn["name"],
            "attributes": jsn["attributes"]
        }

        return output


    def fetchAllMeta(self):
        data = []
        for x in range(self.QUANTITY):
            # print(x)
            dt = self.fetchSingleMeta(number=x)
            data.append(dt)
        # print("Length: {}".format(len(data)))
        return data




meta = NFTMetaStripper(metaId="ipfsID")
data = meta.fetchAllMeta()
