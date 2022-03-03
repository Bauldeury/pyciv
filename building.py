import csv
import common

_buildings = {}
class _building:
    def __init__(self, key):
        self.key = key
        self.name = "Unnamed Building"
        self.description = "Default building description."
        self.hammerCost = 50
        self.maintenance = 1
        self.requires = None
        self.obsoletedBy = None
        self.specials = None
        _buildings[key] = self
        
    def __repr__(self):
        return "C_BUILDING:{}".format(self.key)
        
    @property
    def purchaseCost(self):
        return self.hammerCost*4
    @property
    def sellCost(self):
        return self.hammerCost

def _loadBuidings():
    with open("buildings.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key = row[0]
                bld = _building(key)
                bld.name = row[1]
                bld.description = row [2]
                bld.hammerCost = row[3]
                bld.maintenance = row[4]
                bld.requires = (None if row[5] == '' else row[5])
                bld.obsoletedBy = (None if row[6] == '' else row[6])
                bld.specials = row[7].split(',')
            
class buildingSet:
    def __init__(self):
        self._blds = {}
        self._sps = {}
        self._computeSpecials()
        
    def __repr__(self):
        return "C_BUILDING_SET:{}".format(self._blds)
        
    def _computeSpecials(self):
        self._sps["POP_SUPPORT"] = common.getSpecialValueSum(self._blds,"POP_SUPPORT")
        
        self._sps["INCREASE_TAX_RATE"] = common.getSpecialValueSum(self._blds,"INCREASE_TAX_RATE")
        self._sps["INCREASE_SCIENCE_RATE"] = common.getSpecialValueSum(self._blds,"INCREASE_SCIENCE_RATE")
        self._sps["DECREASE_CORRUPTION"] = common.getSpecialValueSum(self._blds,"DECREASE_CORRUPTION")
        self._sps["DECREASE_INDUSTRIAL_POLLUTION"] = common.getSpecialValueSum(self._blds,"DECREASE_INDUSTRIAL_POLLUTION")
        
        self._sps["FOOD_YIELD"] = common.getSpecialValueSum(self._blds,"FOOD_YIELD")
        self._sps["PRODUCTION_YIELD"] = common.getSpecialValueSum(self._blds,"PRODUCTION_YIELD")
        self._sps["COMMERCE_YIELD"] = common.getSpecialValueSum(self._blds,"COMMERCE_YIELD")
        self._sps["HAPPINESS_YIELD"] = common.getSpecialValueSum(self._blds,"HAPPINESS_YIELD")
        self._sps["DEFENSE_BONUS"] = common.getSpecialValueSum(self._blds,"DEFENSE_BONUS")
        
        self._sps["ALLOW_VETERANS"] = common.getSpecialExists(self._blds,"ALLOW_VETERANS")
        self._sps["FORT"] = common.getSpecialExists(self._blds,"FORT")
        self._sps["NUKE_PROTECTION"] = common.getSpecialExists(self._blds,"NUKE_PROTECTION")
    
    def add(self,buildingKey):
        self._blds[buildingKey] = _buildings[buildingKey]
        self._computeSpecials()
        
    def remove(self,buildingKey):
        self._blds.pop(buildingKey)
        self._computeSpecials()
        
    def build(self,buildingKey):
        if self.canBuild(buildingKey):
            self.add(buildingKey)
        
    def toSet(self):
        return self._blds.copy()
        
    @property
    def count(self):
        return len(self._blds)
    
    
    def canBuild(self,buildingKey):
        if buildingKey in self._blds:
            return False
        
        bld = _buildings[buildingKey]
        
        #TODO: technology requirement
        if bld.requires == False:
            pass
            
        for i in range(len(bld.specials)):
            #pre-existing building requirement
            if bld.specials[i] == "REQUIRE_BUILDING":
                requiredBuildingKey = bld.specials[i+1]
                if requiredBuildingKey not in self._blds:
                    return False
            
            #TODO: water requirement
        
        
        return True
        

_loadBuidings()