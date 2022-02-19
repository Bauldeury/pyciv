class _terrain:
    def __init__(self):
        self.name = "TerrainName"
        self.foodYield = 0
        self.productionYield = 0
        self.commerceYield = 0
        self.travelCost = 1
        self.defensiveBonus = 0
        self.availableResources = set()

class _resource:
    def __init__(self):
        self.name = "ResourceName"
        self.foodYield = 0
        self.productionYield = 0
        self.commerceYield = 0


_terrains = {}
_resources = {}

def _loadTerrains():
    pass
def _loadResources():
    pass
    
class tile:
    def __init__(self):
        self.terrain = "GRASSLANDS"
        self.resource = None
        self.improvement = None
        self.road = False
        self.railroad = False

class map:
    def __init__(self,sizeX,sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.tiles = {}
        for x in range (sizeX):
            for y in range (sizeY):
                self.tiles[(x,y)] = tile()
        
_loadTerrains()
_loadResources()