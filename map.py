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
        self.ttype = 0 #0 for ground, 1 for maritime
        
    def __repr__(self):
        return "C_TERRAIN:{}".format(self.key)

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
    
    def __repr__(self):
        return "C_FEATURE:{}".format(self.key)



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
                t.foodYield = float(row[3])
                t.productionYield = float(row[4])
                t.commerceYield = float(row[5])
                t.travelCost = float(row[6])
                t.defensiveBonus = int(row[7])
                t.availableFeatures = row[8].split(',')
                t.ttype = int(row[9])
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
                f.ftype = int(row[6]) #0 for natural features, 1 for resources, 2 for roads, 3 for other improvements
                f.workAmount = int(row[7]) if row[7] != "" else None
                f.specials = row[8].split(',') if row[8] != "" else None
                _features[f.key] = f
    
class tile:
    def __init__(self):
        self.terrain = _terrains["GRASSLAND"]
        self.features = None
    def __repr__(self):
        return "C_TILE:[{}][{}]".format(self.terrain,self.features)
        
    def getSpecialExists(self,special):
        if self.features == None:
            return False
        else:
            fts = self.features
            for i in fts:
                if fts[i].specials != None :
                    if special in fts[i].specials:
                        output = True
        return False
                        
    def getSpecialValueSum(self,special):
        if self.features == None:
            return 0.0
        else:
            output = 0.0
            fts = self.features
            for i_ft in fts:
                sps = fts[i_ft].specials
                if sps != None:
                    for i_sp in range(len(sps)-1):
                        if special == sps[i_sp]:
                            output += float(sps[i_sp+1])
            return output

    def getSpecialValueProduct(self,special):
        if self.features == None:
            return 1.0
        else:
            output = 1.0
            fts = self.features
            for i_ft in fts:
                sps = fts[i_ft].specials
                if sps != None:
                    for i_sp in range(len(sps)-1):
                        if special == sps[i_sp]:
                            output *= float(sps[i_sp+1])
            return output
        
        
    def addFeature(self,featureKey1):
        bigKey = (featureKey1,self.terrain.key)
        semiKey = (featureKey1,None)
        newFeature = None
        
        if bigKey in _features:
            newFeature = _features[bigKey]   
        elif semiKey in _features:
            newFeature = _features[semiKey]
        
        if newFeature != None:
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
        overwrite = self.getSpecialValueSum("SET_MOVEMENT_COST")
        return self.terrain.travelCost if overwrite == 0 else overwrite
              
    @property
    def foodYield(self):
        output = self.terrain.foodYield + self.getSpecialValueSum("FOOD_YIELD")
        output *= self.getSpecialValueProduct("ALL_MULTIPLIER")
        return int(output)
           
    @property
    def productionYield(self):
        output = self.terrain.productionYield + self.getSpecialValueSum("PRODUCTION_YIELD")
        output *= self.getSpecialValueProduct("ALL_MULTIPLIER")
        return int(output)
           
    @property
    def commerceYield(self):
        output = self.terrain.commerceYield + self.getSpecialValueSum("COMMERCE_YIELD")
        output *= self.getSpecialValueProduct("ALL_MULTIPLIER")
        return int(output)
           
    @property
    def defensiveBonus(self):
        return int(self.terrain.defensiveBonus + self.getSpecialValueSum("DEFENSIVE_BONUS"))
           
    @property
    def ttype(self):
        return self.terrain.ttype
        
        
        


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