import csv

class _terrain:
    def __init__(self):
        self.key = "TERRAIN_KEY"
        self.name = "TerrainName"
        self.description = "TerrainDescription"
        self.foodYield = 0
        self.productionYield = 0
        self.commerceYield = 0
        self.travelCost = 1
        self.defensiveBonus = 0
        self.availableFeatures = set()
        self.isMaritime = False

class _feature:
    def __init__(self):
        self.key = ("FEATURE_KEY","TERRAIN_KEY")
        self.name = "FeatureName"
        self.description = "FeatureDescription"
        self.requires = None
        self.constraints = None
        self.ftype = 0 #0 for natural features, 1 for resources, 2 for roads, 3 for other improvements
        self.workAmount = 50
        self.specials = None



_terrains = {}
_features = {}

def _loadTerrains():
    with open("terrains.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                t = _terrain()
                t.key = row[0]
                t.name = row[1]
                t.description = row[2]
                t.foodYield = row[3]
                t.productionYield = row[4]
                t.commerceYield = row[5]
                t.travelCost = row[6]
                t.defensiveBonus = row[7]
                t.availableFeatures = row[8].split(',')
                t.isMaritime = (row[9]=="yes")
                _terrains[t.key] = t
                
def _loadFeatures():
    with open("features.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                f = _feature()
                f.key =(row[0],row[1] if row[1]!="" else None)
                f.name = row[2]
                f.description = row[3]
                f.requires = row[4] if row[4] != "" else None
                f.constraints = row[5].split(',') if row[5] != "" else None
                f.ftype = row[6] #0 for natural features, 1 for resources, 2 for roads, 3 for other improvements
                f.workAmount = row[7]
                f.specials = row[8].split(',') if row[8] != "" else None
                _features[f.key] = f
    
class tile:
    def __init__(self):
        self.terrain = _terrains["GRASSLAND"]
        self.features = None
        
    def addFeature(self,featureKey1):
        bigKey = (featureKey1,self.terrain.key)
        if bigKey in _features:
            newFeature = _features[bigKey]
            if self.features == None:
                self.features = {newFeature.ftype:newFeature}
            else:
                self.features[newFeature.ftype] = newFeature
    
    def removeFeature(self,ftype):
        if self.features != None:
            self.features.pop(ftype)
            if len(self.features) == 0:
                del self.features
                self.features = None
        
           
    @property
    def name(self):
        return self.terrain.name
           
    @property
    def description(self):
        return self.terrain.description
        
    @property
    def travelCost(self):
        return self.terrain.travelCost
            
        
    @property
    def foodYield(self):
        output = self.terrain.foodYield
        
        if self.features != None:
            for ft in self.features:
                if ft.specials != None :
                    if "FOOD_YIELD" in ft.specials:
                        output += ft[ft.index("FOOD_YIELD")+1]
                
        return output
           
    @property
    def productionYield(self):
        return 1
           
    @property
    def commerceYield(self):
        return 1
           
    @property
    def defensiveBonus(self):
        return 1
           
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
_loadFeatures()