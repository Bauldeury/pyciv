import csv

from . import Common

terrains:"dict[str,Terrain]" = {}
class Terrain:
    def __init__(self, key):
        self.key:str = key
        self.intKey:int = len(terrains)
        self.name = "TerrainName"
        self.description = "TerrainDescription"
        self.foodYield = 0
        self.productionYield = 0
        self.goldYield = 0
        self.travelCost = 1
        self.defensiveBonus = 0 
        '''50 is +50%'''
        self.terrainType = 0
        '''0:ground(default), 1:maritime'''
        self.tags:"list[str]|None" = None


        terrains[self.key] = self
        
    def __repr__(self):
        return "C_TERRAIN:{}".format(self.key)

def _loadTerrains():
    with open(Common.getCommonPath()+"terrains.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                cKey = row.index("key")
                cName = row.index("name")
                cDescription = row.index("description")
                cFoodYield = row.index("foodYield")
                cProductionYield = row.index("productionYield")
                cGoldYield = row.index("goldYield")
                cTravelCost = row.index("travelCost")
                cDefensiveBonus = row.index("defensiveBonus")
                cTerrainType = row.index("terrainType")

            else:
                key = row[cKey]
                t = Terrain(key)
                
                t.name = row[cName]
                t.description = row[cDescription]
                t.foodYield = float(row[cFoodYield])
                t.productionYield = float(row[cProductionYield])
                t.goldYield = float(row[cGoldYield])
                t.travelCost = float(row[cTravelCost])
                t.defensiveBonus = int(row[cDefensiveBonus])
                t.terrainType = int(row[cTerrainType])
                
class Helper:
    def intToTerrain(intKey:int) -> "Terrain|None":
        for item in terrains.values():
            if item.intKey == intKey:
                return item
        return None
        
_loadTerrains()