import csv

_techs = {}
class tech:
    def __init__(self,key):
        self.key = key
        _techs[self.key] = self
        
        self.name = "TechName"
        self.description = "TechDesc"
        self.cost = 100
        self.requires = -1#list of tech keys, or None if available from the start, or -1 if impossible to search
        
        
def _loadTechs():
    with open("techs.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key = row[0]
                th = tech(key)
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
    
    
class techSet:
    def __init__(self):
        self._ths = {}
        
    def __repr__(self):
        return "C_TECH_SET:{}".format(self._ths.keys())
        
    def add(self,techKey):
        self._ths[techKey] = _techs[techKey]
        
    def addBulk(self,techKeySet):
        for techKey in techKeySet:
            self._ths[techKey] = _techs[techKey]
        
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
        
        th = _techs[techKey]
        
        if th.requires == -1:
            return False
        
        if th.requires != None:
            for t in th.requires:
                if t not in self._ths:
                    return False
        
        
        return True
        
    def getSearcheables(self):
        return set(x for x in _techs if self.canSearch(x))
       
    @property
    def count(self):
        return len(self._ths)
        
    def contains(self,techKey):
        return (techKey in self._ths)
    
_loadTechs()