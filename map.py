import csv

class _terrain:
    def __init__(self):
        self.name = "TerrainName"
        self.description = "TerrainDescription"
        self.foodYield = 0
        self.productionYield = 0
        self.commerceYield = 0
        self.travelCost = 1
        self.defensiveBonus = 0
        self.availableResources = set()
        self.isMaritime = False

class _resource:
    def __init__(self):
        self.name = "ResourceName"
        self.description = "ResourceDescription"
        self.foodYield = 0
        self.productionYield = 0
        self.commerceYield = 0
        self.isTradable = True


_terrains = {}
_resources = {}

def _loadTerrains():
    with open("terrains.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                t = _terrain()
                t.name = row[1]
                t.description = row[2]
                t.foodYield = row[3]
                t.productionYield = row[4]
                t.commerceYield = row[5]
                t.travelCost = row[6]
                t.defensiveBonus = row[7]
                t.availableResources = row[8].split(',')
                t.isMaritime = (row[9]=="yes")
                _terrains[row[0]] = t
                
def _loadResources():
    with open("resources.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                r = _resource()
                r.name = row[1]
                r.description = row[2]
                r.foodYield = row[3]
                r.productionYield = row[4]
                r.commerceYield = row[5]
                r.isTradable = (row[6]=="yes")
                _resources[row[0]] = r
    
class tile:
    def __init__(self):
        self.terrain = _terrains["GRASSLAND"]
        self.resources = None
        self.improvements = None
        
           
    @property
    def name(self):
        return self.terrain.name
           
    @property
    def description(self):
        return self.terrain.description
        
    @property
    def travelCost(self):
        return self.terrain.travelCost
            
    # @travelCost.setter       
    # def travelCost(self,value):
        # print("travelCost is read-only")
        
    @property
    def foodYield(self):
        output = self.terrain.foodYield
        
        if self.resources != None:
            output+= sum(x.foodYield for x in self.resource)
            
        im = self.improvements
        if im != None:
            if "FOOD_YIELD" in im:
                output += im[im.index("FOOD_YIELD")+1]
                
        return output
           
    @property
    def productionYield(self):
        output = self.terrain.productionYield
        
        if self.resources != None:
            output+= sum(x.productionYield for x in self.resource)
            
        im = self.improvements
        if im != None:
            if "PRODUCTION_YIELD" in im:
                output += im[im.index("PRODUCTION_YIELD")+1]
                
        return output
           
    @property
    def commerceYield(self):
        output = self.terrain.commerceYield
        
        if self.resources != None:
            output+= sum(x.commerceYield for x in self.resource)
            
        im = self.improvements
        if im != None:
            if "COMMERCE_YIELD" in im:
                output += im[im.index("COMMERCE_YIELD")+1]
                
        return output
           
    @property
    def defensiveBonus(self):
        output = self.terrain.defensiveBonus
        
        im = self.improvements
        if im != None:
            if "DEFENSIVE_BONUS" in im:
                output += im[im.index("DEFENSIVE_BONUS")+1]
                
        return output
           
    @property
    def isMaritime(self):
        return self.terrain.isMaritime
        
        
        


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