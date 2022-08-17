import csv

from . import Common

unitTypes:"dict[str,UnitType]" = {}
class UnitType:
    def __init__(self,key:str):
        self.key:str = key
        self.intKey:int = len(unitTypes)
        unitTypes[self.key] = self
        
        self.name:str = "UnittypeName"
        self.description:str = "UnittypeDescription"
        
        self.maxLife:int = 100
        self.maxMove:float = 1.0
        self.strength:int = 10
        self.tags:"list[str]" = list()
        self.specials:"list[str]" = list()
        
        self.cost:int = 10 #number of hammers
        self.requiresTech:"str|None" = None #technology
    
    def __repr__(self):
        return "C_UNITTYPE:{}".format(self.key)

units:"set[Unit]" = set()
class Unit:
    def __init__(self, unitType:UnitType, owner:int = 0, pos:"tuple[int,int]" = (0,0)):
        self.unitType = unitType
        self.owner = owner
        self.pos = pos
        
        self.name:str = self.unitType.name
        self.curLife:int = self.maxLife
        self.curMove:float = self.maxMove
        
        units.add(self)
    
    def __repr__(self):
        return "C_UNIT:{},owner{},pos{}".format(self.name,self.owner,self.pos)
        
    def destroy(self):
        if self in units:
            units.remove(self)
        del self
        
    def endTurn(self):
        self.curMove = self.maxMove
        if self.curLive < self.maxLife:
            self.curLive = min(self.curLive + 5, self.maxLife)
            
     
    @property
    def maxLife(self):
        return self.unitType.maxLife
        
    @property
    def maxMove(self):
        return self.unitType.maxMove
        
    @property
    def strength(self):
        return self.unitType.strength * self.curLife/self.maxLife
        
    @property
    def specials(self):
        return self.unitType.specials

    @property
    def tags(self):
        return self.unitType.tags

def _loadUnitsTypes():
    with open(Common.getCommonPath()+"units.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                cKey = row.index("key")
                cName = row.index("name")
                cDescription = row.index("description")
                cStrength = row.index("strength")
                cMove = row.index("move")
                cCost = row.index("cost")
                cRequiresTech = row.index("requiresTech")
                cTags = row.index("tags")
                cSpecials = row.index("specials")
            else:
                key = row[cKey]
                f = UnitType(key)

                f.name = row[cName]
                f.description = row[cDescription]
                f.requiresTech = row[cRequiresTech] if row[cRequiresTech] != "" else None
                f.strength = int(row[cStrength])
                f.maxMove = int(row[cMove])
                f.cost = int(row[cCost])
                f.specials = row[cSpecials].split(',') if row[cSpecials] != "" else []
                f.tags = row[cTags].split(',') if row[cTags] != "" else []

class Helper:
    def getUnitsOnPos(pos:"tuple[int,int]"):
        return set(x for x in units if x.pos == pos)
        
    def getUnitsOfOwner(ownerKey:int):
        return set(x for x in units if x.owner == ownerKey)
        
    def intToUnitType(intKey):
        for item in unitTypes.values():
            if item.intKey == intKey:
                return item
        return None


_loadUnitsTypes() 