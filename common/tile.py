import math

from . import common
from . import terrain
from . import feature

class tile:
    def __init__(self):
        self.terrain:terrain.terrain = terrain.terrains["GRASSLAND"]
        self.features = None
        
    def __repr__(self):
        return "C_TILE:[{}][{}]".format(self.terrain,self.features)
        
    def getSpecialExists(self,special):
        return common.getSpecialExists(self.features,special)
                        
    def getSpecialValueSum(self,special):
        return common.getSpecialValueSum(self.features,special)

    def getSpecialValueProduct(self,special):
        return common.getSpecialValueProduct(self.features,special)
        
        
    def addFeature(self,featureKey1):
        bigKey = (featureKey1,self.terrain.key)
        semiKey = (featureKey1,None)
        newFeature:feature.feature = None
        
        if bigKey in feature.features:
            newFeature = feature.features[bigKey]   
        elif semiKey in feature.features:
            newFeature = feature.features[semiKey]
        
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
        
      
    