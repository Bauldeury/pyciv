_civilizations = {}
_endTurnListener = set()

class Civilization:
    
    def __init__(self,key = "NEW"):
        '''Civilization constructor
        
        key -- unique ID. Leave "NEW" to auto-attribute the next id.'''
        if key == "NEW":
            key = 0
            while key in _civilizations:
                key += 1

            self.key = key
        else:
            self.key = key

        _civilizations[self.key] = self
        self.canDoDiplomacy = True
        
        self.name = "CivName"
        self.leaderName = "LeaderName"
        self.adjective = "civnamian"
        self.color = "FF0000"
        self.color2 = "FFFF00"
        
        self.techs = set()
        self.gold = 100
        
        self.isTurnFinished = False
    
    def __repr__(self):
        return "C_civilization#{}:{}".format(self.key,self.name)
        
    def endTurn(self, forcedByMain = False):
        if self.isTurnFinished == True:
            return
        
        self.isTurnFinished = True
        
        if (forcedByMain == False):
            if Helper._areAllcivilizationTurnFinished():
                for method in _endTurnListener:
                    method()
        
    def startTurn(self):
        self.isTurnFinished = False


class Helper():
    def endTurn():
        for i_civilization in _civilizations:
            _civilizations[i_civilization].endTurn(forcedByMain = True)
            
    def startTurn():
        for i_civilization in _civilizations:
            _civilizations[i_civilization].startTurn()
            
    def getcivilization(key_civilization:int)->Civilization:
        return _civilizations[key_civilization]
        
    def _areAllcivilizationTurnFinished():
        for i_civilization in _civilizations:
            if _civilizations[i_civilization].isTurnFinished == False:
                return False
        return True
        
    def registerEndTurnListener(method):
        _endTurnListener.add(method)
          
    def unregisterEndTurnListener(method):
        _endTurnListener.remove(method)
        