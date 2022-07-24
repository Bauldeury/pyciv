import csv

from . import common

terrains = {}
class terrain:
    def __init__(self, key):
        self.key = key
        self.byteKey = int.to_bytes(len(terrains),length=1,byteorder='big')
        self.name = "TerrainName"
        self.description = "TerrainDescription"
        self.foodYield = 0
        self.productionYield = 0
        self.commerceYield = 0
        self.travelCost = 1
        self.defensiveBonus = 0
        self.availableFeatures = set()
        self.ttype = 0 #0 for ground, 1 for maritime
        terrains[self.key] = self
        
    def __repr__(self):
        return "C_TERRAIN:{}".format(self.key)

def _loadTerrains():
    with open(common.getCommonPath()+"terrains.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key = row[0]
                t = terrain(key)
                
                t.name = row[1]
                t.description = row[2]
                t.foodYield = float(row[3])
                t.productionYield = float(row[4])
                t.commerceYield = float(row[5])
                t.travelCost = float(row[6])
                t.defensiveBonus = int(row[7])
                t.availableFeatures = row[8].split(',')
                t.ttype = int(row[9])
                
class helper:
    def byteToTerrain(byteKey):
        for item in terrains.values():
            if item.byteKey == byteKey:
                return item
        return None
        
_loadTerrains()