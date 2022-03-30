_civilizations = {}
_endTurnListener = set()

class civilization:
    _civilizationsNextKey = 0
    
    def __init__(self):
        self.key = civilization._civilizationsNextKey
        civilization._civilizationsNextKey += 1
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
            if helper._areAllcivilizationTurnFinished():
                for method in _endTurnListener:
                    method()
        
    def startTurn(self):
        self.isTurnFinished = False


class helper():
    def endTurn():
        for i_civilization in _civilizations:
            _civilizations[i_civilization].endTurn(forcedByMain = True)
            
    def startTurn():
        for i_civilization in _civilizations:
            _civilizations[i_civilization].startTurn()
            
    def getcivilization(key_civilization):
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
        