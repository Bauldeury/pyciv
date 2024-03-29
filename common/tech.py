import csv

from . import Common

techs:"dict[str,Tech]" = {}
class Tech:
    def __init__(self,key:str):
        self.key:str = key
        self.intKey:int = len(techs)
        techs[self.key] = self
        
        self.name = "TechName"
        self.description = "TechDesc"
        self.cost = 100
        self.requires = -1#list of tech keys, or None if available from the start, or -1 if impossible to search
        
        
def _loadTechs():
    with open(Common.getCommonPath()+"techs.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key = row[0]
                th = Tech(key)
                th.name = row[1]
                th.description = row [2]
                th.cost = row[3]
                
                r_requires = row[4]
                if r_requires == "-1":
                    th.requires = -1
                elif r_requires == "":
                    th.requires = None
                else:
                    th.requires = r_requires.split(',')
    
    
class TechSet:
    def __init__(self):
        self._ths:"dict[str,Tech]" = {}
        
    def __repr__(self):
        return "C_TECH_SET:{}".format(self._ths.keys())
        
    def add(self,techKey:str):
        self._ths[techKey] = techs[techKey]
        
    def addBulk(self,techKeySet:"set[str]"):
        for techKey in techKeySet:
            self._ths[techKey] = techs[techKey]
        
    def remove(self,techKey):
        self._ths.pop(techKey)
        
    def removeBulk(self,techKeySet):
        for techKey in techKeySet:
            self._ths.pop(techKey)
        
    def toSet(self):
        return self._ths.copy()
     
    
    def canSearch(self,techKey):
        if techKey in self._ths:
            return False
        
        th = techs[techKey]
        
        if th.requires == -1:
            return False
        
        if th.requires != None:
            for t in th.requires:
                if t not in self._ths:
                    return False
        
        
        return True
        
    def getSearcheables(self):
        return set(x for x in techs if self.canSearch(x))
       
    @property
    def count(self):
        return len(self._ths)
        
    def contains(self,techKey):
        return (techKey in self._ths)
    
class Helper:
    def byteToTech(byteKey):
        for item in techs.values():
            if item.byteKey == byteKey:
                return item
        return None
        
_loadTechs()