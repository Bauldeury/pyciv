import csv

tileArtDefines: "dict[str,TileArtDefine]" = dict()
unitArtDefines: "dict[str,UnitArtDefine]" = dict()


class TileArtDefine:
    def __init__(self, key: str, xy: "tuple[int,int]", layer: int):
        self.key: str = key
        self.xy = xy
        self.layer = layer

class UnitArtDefine:
    def __init__(self, key: str, xy: "tuple[int,int]"):
        self.key: str = key
        self.xy = xy


def _loadTileArtDefine():
    with open("client/assets/tilesArtDefine.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                cKey = row.index("key")
                cX = row.index("x")
                cY = row.index("y")
                cLayer = row.index("layer")
            else:
                key = row[cKey]
                xy = (int(row[cX]),int(row[cY]))
                layer = int(row[cLayer])
                tileArtDefine = TileArtDefine(key, xy, layer)

                tileArtDefines[key] = tileArtDefine

def _loadUnitArtDefine():
    with open("client/assets/unitsArtDefine.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                cKey = row.index("key")
                cX = row.index("x")
                cY = row.index("y")
            else:
                key = row[cKey]
                xy = (int(row[cX]),int(row[cY]))
                unitArtDefine = UnitArtDefine(key, xy)

                unitArtDefines[key] = unitArtDefine


_loadTileArtDefine()
_loadUnitArtDefine()
