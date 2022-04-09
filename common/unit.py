import csv

from . import common

_unitTypes = {}
class _unitType:
    def __init__(self):
        self.key = "UNITTYPE_KEY"
        self.byteKey = int.to_bytes(len(_unitTypes),length=1,byteorder='big')
        _unitTypes[self.key] = self
        
        self.name = "UnittypeName"
        
        self.maxLife = 10
        self.maxMove = 1.0
        self.attack = 1
        self.defense = 1
        self.specials = None #list of strings
        
        self.cost = 10 #number of hammers
        self.requires = None #technology
    
    def __repr__(self):
        return "C_UNITTYPE:{}".format(self.key)

_units = set()
class unit:
    def __init__(self, unitType, owner = 0, pos = (0,0)):
        self.unitType = unitType
        self.owner = owner
        self.pos = pos
        
        self.name = self.unitType.name
        self.curLife = self.maxLife
        self.curMove = self.maxMove
        
        _units.add(self)
    
    def __repr__(self):
        return "C_UNIT:{},owner{},pos{}".format(self.name,self.owner,self.pos)
        
    def destroy(self):
        _units.remove(self)
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
    def attack(self):
        return self.unitType.attack
        
    @property
    def defense(self):
        return self.unitType.defense
        
    @property
    def specials(self):
        return self.unitType.specials

class helper:
    def getUnitsOnPos(pos):
        return set(x for x in _units if x.pos == pos)
        
    def getUnitsOfOwner(ownerKey):
        return set(x for x in _units if x.owner == ownerKey)
        
    def byteToUnitType(byteKey):
        for item in _unitTypes.values():
            if item.byteKey == byteKey:
                return item
        return None