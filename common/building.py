import csv

from . import Common

_buildingTypes:"dict[str,BuildingType]" = {}
class BuildingType:
    def __init__(self, key):
        self.key = key
        self.intKey = len(_buildingTypes)
        self.name = "Unnamed Building"
        self.description = "Default building description."
        self.hammerCost = 50
        self.maintenance = 1
        self.requires = None
        self.obsoletedBy = None
        self.specials = None
        _buildingTypes[key] = self
        
    def __repr__(self):
        return "C_BUILDING:{}".format(self.key)
        
    @property
    def purchaseCost(self):
        return self.hammerCost*4
    @property
    def sellCost(self):
        return self.hammerCost

def _loadBuidings():
    with open(Common.getCommonPath()+"buildings.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key = row[0]
                bld = BuildingType(key)
                bld.name = row[1]
                bld.description = row [2]
                bld.hammerCost = row[3]
                bld.maintenance = row[4]
                bld.requires = (None if row[5] == '' else row[5])
                bld.obsoletedBy = (None if row[6] == '' else row[6])
                bld.specials = (None if row[7] == '' else row[7].split(','))
            
class BuildingSet:
    def __init__(self, city = None):
        self._blds = {}
        self._sps = {}
        self._computeSpecials()
        self.city = city
        
    def __repr__(self):
        return "C_BUILDING_SET:{}".format(self._blds.keys())
        
    def _computeSpecials(self):
        self._sps["POP_SUPPORT"] = int(Common.getSpecialValueSum(self._blds,"POP_SUPPORT"))
        
        self._sps["INCREASE_TAX_RATE"] = int(Common.getSpecialValueSum(self._blds,"INCREASE_TAX_RATE"))
        self._sps["INCREASE_SCIENCE_RATE"] = int(Common.getSpecialValueSum(self._blds,"INCREASE_SCIENCE_RATE"))
        self._sps["DECREASE_CORRUPTION"] = int(Common.getSpecialValueSum(self._blds,"DECREASE_CORRUPTION"))
        self._sps["DECREASE_INDUSTRIAL_POLLUTION"] = int(Common.getSpecialValueSum(self._blds,"DECREASE_INDUSTRIAL_POLLUTION"))
        self._sps["DEFENSE_BONUS"] = int(Common.getSpecialValueSum(self._blds,"DEFENSE_BONUS"))
        
        self._sps["FOOD_YIELD"] = int(Common.getSpecialValueSum(self._blds,"FOOD_YIELD"))
        self._sps["PRODUCTION_YIELD"] = int(Common.getSpecialValueSum(self._blds,"PRODUCTION_YIELD"))
        self._sps["COMMERCE_YIELD"] = int(Common.getSpecialValueSum(self._blds,"COMMERCE_YIELD"))
        self._sps["HAPPINESS_YIELD"] = int(Common.getSpecialValueSum(self._blds,"HAPPINESS_YIELD"))
        
        self._sps["ALLOW_VETERANS"] = Common.getSpecialExists(self._blds,"ALLOW_VETERANS")
        self._sps["FORT"] = Common.getSpecialExists(self._blds,"FORT")
        self._sps["NUKE_PROTECTION"] = Common.getSpecialExists(self._blds,"NUKE_PROTECTION")
    
    def add(self,buildingKey):
        self._blds[buildingKey] = _buildingTypes[buildingKey]
        self._computeSpecials()
        
    def addBulk(self,buildingKeySet):
        for buildingKey in buildingKeySet:
            self._blds[buildingKey] = _buildingTypes[buildingKey]
        self._computeSpecials()
        
    def remove(self,buildingKey):
        self._blds.pop(buildingKey)
        self._computeSpecials()
        
    def removeBulk(self,buildingKeySet):
        for buildingKey in buildingKeySet:
            self._blds.pop(buildingKey)
        self._computeSpecials()
        
    def build(self,buildingKey):
        if self.canBuild(buildingKey):
            self.add(buildingKey)
        
    def toSet(self):
        return self._blds.copy()
     
    
    def canBuild(self,buildingKey):
        if buildingKey in self._blds:
            return False
        
        bld = _buildingTypes[buildingKey]
        
        #TODO: technology requirement
        if bld.requires == None:
            pass
            
        for i in range(len(bld.specials)):
            #pre-existing building requirement
            if bld.specials[i] == "REQUIRE_BUILDING":
                requiredBuildingKey = bld.specials[i+1]
                if requiredBuildingKey not in self._blds:
                    return False
            
            #TODO: water requirement
        
        
        return True
        
    def getBuildables(self):
        return set(x for x in _buildingTypes if self.canBuild(x))
       
    @property
    def count(self):
        return len(self._blds)
        
    @property
    def specials(self):
        return self._sps.copy()
        
    def special(self,specialKey):
        return self._sps[specialKey]
        
    @property
    def tile(self):
        return self.city.tile

class helper:
    def byteToBuilding(byteKey):
        for item in _buildingTypes.values():
            if item.byteKey == byteKey:
                return item
        return None


_loadBuidings()