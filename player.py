_players = {}
_endTurnListener = set()

class player:
    _playersNextKey = 0
    
    def __init__(self):
        self.key = player._playersNextKey
        player._playersNextKey += 1
        _players[self.key] = self
        
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
        return "C_PLAYER#{}:{}".format(self.key,self.name)
        
    def endTurn(self):
        if self.isTurnFinished == True:
            return
        
        self.isTurnFinished = True
        
        if helper._areAllPlayerTurnFinished():
            for method in _endTurnListener:
                method()
        
    def startTurn(self):
        self.isTurnFinished = False


class helper():
    def endTurn():
        for i_player in _players:
            _players[i_player].endTurn()
            
    def startTurn():
        for i_player in _players:
            _players[i_player].startTurn()
            
    def getPlayer(key_player):
        return _players[key_player]
        
    def _areAllPlayerTurnFinished():
        for i_player in _players:
            if _players[i_player].isTurnFinished == False:
                return False
        return True
        
    def registerEndTurnListener(method):
        _endTurnListener.add(method)
          
    def unregisterEndTurnListener(method):
        _endTurnListener.remove(method)
        