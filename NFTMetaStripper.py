import requests
import json


class NFTMetaStripper:
    META = {}
    META_STATS = {}
    META_LINK = ""

    DEBUG = False


    def __init__(self, debug=False):
        """ Sets the debug mode of the Class
        """
        self.DEBUG = debug


    def _formatAddress(self, address, id, mode=""):
        """ Takes the web address and ID of the NFT and creates the address to use
        for the request object to return the json. Ypu can provide a mode which will
        format different addresses.
        """
        if address[:15] == "https://ipfs.io" or mode == "ipfs":
            return "https://ipfs.io/ipfs/{}".format(metaId)

        if mode == "" or mode == "standard":
            return "{}/{}".format(address, id)

        if mode == "standard-json":
            return "{}/{}".format(address, id)

        print("No valid address supplied")
        return


    def _debugPrint(self, message):
        """ Prints the message to the screen if debug mode is on
        """
        if self.DEBUG == True:
            print(message)


    def _fetchRaw(self, address):
        """ Fetches the raw json and returns it. Intended for debugging only.
        """
        r = requests.get(address)
        return json.loads(r.text)


    def extract(self, baseAddress, collectionCount, projectName, mode=""):
        """ Loops over the collection of NFTs meta addresses, scrapes and
        organises the data into the META and META_STATS variables for use later.
        """
        if not (isinstance(baseAddress, str) and isinstance(collectionCount, int) and isinstance(projectName, str)):
            print("The provided variables were not of the correct types")
            return

        self._debugPrint("Extracting {} records from {} at {}".format(collectionCount, projectName, baseAddress))
        self._debugPrint(self._fetchRaw(self._formatAddress(baseAddress, 1, mode)))

        self.META[projectName] = []
        print("Extracting JSON for {}".format(projectName))

        for i in range(collectionCount):
            self._debugPrint("Running for Item: {}".format(i))

            formattedAddress = self._formatAddress(baseAddress, i, mode)
            jsn = self._fetchSingle(formattedAddress)

            self.META[projectName].append(jsn)

            self._calculateStats(jsn["attributes"], projectName, i)

        print("Extracted {} records\n".format(len(self.META[projectName])))


    def printMeta(self, projectName=""):
        """ Prints the meta data that has been processed by the class. You can provide
        a specicific project name too.
        """
        if projectName == "":
            for item in self.META:
                print(item, ": ", len(self.META[item]))
        else:
            if self.META[projectName]:
                for item in self.META[projectName]:
                    print(item)


    def printMetaStats(self, projectName=""):
        """ Prints the meta statistics and formatted data that has been processed
        by the class. You can provide a specicific project name too.
        """
        if projectName == "":
            print(self.META_STATS)
            for item in self.META_STATS:
                print(item, ": ", len(self.META_STATS[item]))
        else:
            if self.META_STATS[projectName]["attributes"]:
                for attr in self.META_STATS[projectName]["attributes"]:
                    for item in self.META_STATS[projectName]["attributes"][attr]:
                        print(attr, item, len(self.META_STATS[projectName]["attributes"][attr][item]), self.META_STATS[projectName]["attributes"][attr][item])


    def _fetchSingle(self, address):
        """ fetches the json data from the address provided and formats it into a
        useable format.
        """
        r = requests.get(address)
        jsn = json.loads(r.text)

        if jsn["image"][:5] != "https":
            if jsn["image"][:7] == "ipfs://":
                jsn["image"] = self._convertIpfsImgAddress(jsn["image"])

        output = {
            "image": jsn["image"],
            "name": jsn["name"],
            "attributes": self._calculateAttributes(jsn["attributes"])
        }
        return output


    def _convertIpfsImgAddress(self, metaImageString):
        """ Converts the meta address into the web address for the meta image
        """
        return "https://ipfs.io/ipfs/{}".format(metaImageString[7:])


    def _calculateAttributes(self, attributes):
        """ Loops through the scraped attributes and formats them into a basic
        json object.
        """
        output = {}

        for attr in attributes:
            output[attr["trait_type"]] = attr["value"]

        return output


    def _calculateStats(self, attributes, projectName, id):
        """ Organises the NFT collection into a list of attributes and adds the
        IDs of the NFT to an array for each attribute.
        """
        if projectName not in self.META_STATS:
            self.META_STATS[projectName] = {
                "attributes": {}
            }

        for attr in attributes:
            if attr in self.META_STATS[projectName]["attributes"]:
                pass
            else:
                self.META_STATS[projectName]["attributes"][attr] = {}

            if attributes[attr] in self.META_STATS[projectName]["attributes"][attr]:
                self.META_STATS[projectName]["attributes"][attr][attributes[attr]].append(id)
            else:
                self.META_STATS[projectName]["attributes"][attr][attributes[attr]] = []
                self.META_STATS[projectName]["attributes"][attr][attributes[attr]].append(id)




""" Example of how to use for the Little Lemon Friends NFT """
meta = NFTMetaStripper(debug=True)
meta.extract("https://us-central1-little-lemon-friends.cloudfunctions.net/lemon-metadata-api", 10, "Little Lemon Friends")
meta.printMeta("Little Lemon Friends")
meta.printMetaStats("Little Lemon Friends")
