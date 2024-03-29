print(" ____  __    __  ____  ___ __      __")
print("|  _ \ \ \  / / / ___//_ _/\ \    / /")
print("| |_) | \ \/ / | |     | |  \ \  / / ")
print("|  __/   |  |  | |___  | |   \ \/ /  ")
print("|_|      |__|   \____//___/   \__/   ")
print()

from . import Player  

from . import Civilization  
from . import Tilemap
from . import City
from . import Terrain
from . import Feature
from . import Unit
from . import Common

class Game:

    #vars


    def __init__(self):
        Civilization.Helper.registerEndTurnListener(self.endTurn)
        Player.Helper.sendInfoMethod = self.executeInfo

        self.turn:int = 0
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
        City.Helper.endTurn()
        Civilization.Helper.endTurn()
        
        self.turn += 1
        self._advanceYear()
        Common.updateId += 1
        
        print("TURN {}: YEAR {}".format(self.turn,self.currentYear))
        Civilization.Helper.startTurn()

    #networking
    def executeCmd(self,sender: int,cmd:str):
        '''from SERVER to GAME'''

        if cmd == "getmapsize":
            self._sendInfo({sender},"returnmapsize {} {}".format(Tilemap.tilemaps[0].sizeX,Tilemap.tilemaps[0].sizeY))
        else:
            self._sendCmd(sender,cmd)

    def _sendCmd(self,playerId:int,cmd:str):
        '''from GAME to PLAYERHELPER'''
        Player.Helper.executeCmd(playerId,cmd)

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
        Tilemap.tilemaps[0] = Tilemap.Tilemap(10,10)
        Tilemap.tilemaps[0].tiles[(1,2)].features.append(Feature.features["MINE"])
        Tilemap.tilemaps[0].tiles[(2,2)].features.append(Feature.features["MINE"])
        for i in range(5):
            Tilemap.tilemaps[0].tiles[(2,i)].terrain = Terrain.terrains["ARCTIC"]
            Tilemap.tilemaps[0].tiles[(i,2)].features.append(Feature.features["RAILROAD"])
            
        
        p0 = Civilization.Civilization(-1)
        p0.name = "Barbarians"
        p0.leaderName = "Barbarator"
        p0.adjective = "barbarian"
        p0.color = "C31A1A"
        p0.color2 = "393939"
        p0.canDoDiplomacy = False
        
        p1 = Civilization.Civilization()
        p1.name = "Francia"
        p1.leaderName = "civilization"
        p1.adjective = "frank"
        p1.color = "2E63CD"
        p1.color2 = "393939"
        
        p2 = Civilization.Civilization()
        p2.name = "Holy Roman Empire"
        p2.leaderName = "Barberousse"
        p2.adjective = "holy roman"
        p2.color = "EED221"
        p2.color2 = "393939"

        
        c1 = City.City(name = "Paris", owner = p1.key, pos = (1,1))
        
        
        c2 = City.City(name = "Berlin", owner = p2.key, pos = (5,5))