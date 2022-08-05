print(" ____  __    __  ____  ___ __      __")
print("|  _ \ \ \  / / / ___//_ _/\ \    / /")
print("| |_) | \ \/ / | |     | |  \ \  / / ")
print("|  __/   |  |  | |___  | |   \ \/ /  ")
print("|_|      |__|   \____//___/   \__/   ")
print()

from . import player  

from . import civilization  
from . import tech
from . import mymap

from . import city
from . import building

from . import unit

class game:

    #vars


    def __init__(self):
        civilization.helper.registerEndTurnListener(self.endTurn)
        player.helper.sendInfoMethod = self.executeInfo

        self.turn = 0
        self._loadScenario1()
        self.sendInfoMethod = None

        print ("Game Started.")
        
    def _advanceYear(self):

        if self.currentYear < -2000:
            self.currentYear += 100
            
        elif self.currentYear < 0:
            self.currentYear += 50
            
        elif self.currentYear < 1000:
            self.currentYear += 25
            
        elif self.currentYear < 1500:
            self.currentYear += 10
            
        elif self.currentYear < 1750:
            self.currentYear += 5
            
        elif self.currentYear < 1850:
            self.currentYear += 2
            
        else:
            self.currentYear += 1

    def endTurn(self):        
        city.helper.endTurn()
        civilization.helper.endTurn()
        
        self.turn += 1
        self._advanceYear()
        
        print("TURN {}: YEAR {}".format(self.turn,self.currentYear))
        civilization.helper.startTurn()

    #networking
    def executeCmd(self,sender: int,cmd:str):
        '''from SERVER to GAME'''

        if cmd == "getmapsize":
            self._sendInfo({sender},"mapsize {} {}".format(self.mp.sizeX,self.mp.sizeY))
        else:
            self._sendCmd(sender,cmd)

    def _sendCmd(self,playerId:int,cmd:str):
        '''from GAME to PLAYERHELPER'''
        player.helper.executeCmd(playerId,cmd)

    def executeInfo(self,target,info:str):
        '''from PLAYERHELPER to GAME
        
        target must be either "ALL", "NONE", or a list of playerID'''
        self._sendInfo(target,info)

    def _sendInfo(self,playerId,info:str):
        '''from GAME to SERVER
        
        target must be either "ALL", "NONE", or a list of playerID'''
        
        if self.sendInfoMethod != None:
            self.sendInfoMethod(playerId,info)
        else:
            raise Exception("sendInfoMethod not set")

    #scenario

    def _loadScenario1(self):
        self.currentYear = -8000
        self.mp = mymap.mymap(25,25)
        
        p0 = civilization.civilization(-1)
        p0.name = "Barbarians"
        p0.leaderName = "Barbarator"
        p0.adjective = "barbarian"
        p0.color = "C31A1A"
        p0.color2 = "393939"
        p0.canDoDiplomacy = False
        
        p1 = civilization.civilization()
        p1.name = "Francia"
        p1.leaderName = "civilization"
        p1.adjective = "frank"
        p1.color = "2E63CD"
        p1.color2 = "393939"
        
        p2 = civilization.civilization()
        p2.name = "Holy Roman Empire"
        p2.leaderName = "Barberousse"
        p2.adjective = "holy roman"
        p2.color = "EED221"
        p2.color2 = "393939"

        
        c1 = city.city(name = "Paris", owner = p1.key, pos = (1,1))
        
        
        c2 = city.city(name = "Berlin", owner = p2.key, pos = (5,5))