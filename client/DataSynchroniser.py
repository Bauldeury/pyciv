from client import Client

from common import Tile
from common import Tilemap
from common import Terrain
from common import Feature
from common import Common


class DataSynchroniser:
    playerId:"int|None"=None

    def __init__(self, client: "Client.Client"):
        self.client = client

    def executeInfo(self, info: str):
        if info[0:13] == "returnbindok ":
            self._onBind(int(info.split(" ")[1]))
        elif info == "returnunbindok":
            self._onUnbind()
        elif info[0:14] == "returnmapsize ":
            _, x, y = info.split(" ")
            Tilemap.Tilemap(int(x), int(y), 0)
            self.sendCmd("getupdate -1")
        elif info[0:13] == "returnupdate ":
            strings = info.split(" ")
            Common.updateId = int(strings[1])
            for string in strings:
                if string[0] == "t":
                    self._updateTileFromString(string)
            

    def sendCmd(self, cmd: str):
        self.client.executeCmd(cmd)

    def _onBind(self, playerId: int):
        DataSynchroniser.playerId = playerId

        # get initial infos
        self.sendCmd("getmapsize")

    def _onUnbind(self):
        DataSynchroniser.playerId = None

        # clear data
        if Tilemap.tilemaps[0] != None:
            del Tilemap.tilemaps[0]


    def _updateTileFromString(self, string: str):
        """reads and works out strings like this: t[x%][y%][u:unexplored][o:fogofwar][t%:terrainID][f%:featureID]"""
        args = Common.decomposeStrToArgs(
            string[1:], boolArgs=["u", "o"], intArgs=["x", "y", "t"], strArgs=["f"]
        )

        coord = (int(args["x"]), int(args["y"]))
        tile = Tile.Tile()
        tile.updateID = Common.updateId
        tile.terrain = Terrain.Helper.intToTerrain(int(args["t"]))
        if "f" in args:
            for f in args["f"].split(","):
                tile.features.append(Feature.Helper.intToFeature(int(f)))

        Tilemap.tilemaps[0].tiles[coord] = tile