import common.Common as Common
from common.Tilemap import Tilemap


class Player:
    _players = {}

    def __init__(self,playerId):
        if playerId in Player._players:
            raise Exception("PlayerID already existing")

        self.playerId = playerId
        Player._players[self.playerId] = self

    def __del__(self):
        if self.playerId in Player._players: #most of the time no, it's called from the player helper and already deleted
            del Player._players[self.playerId]

    def __repr__(self):
        return "C_player#{}".format(self.playerId)

    def executeCmd(self,cmd:str):
        '''from PLAYERHELPER to PLAYER'''

        if cmd.lower() == "ping player": #test
            self._sendInfo("player pong")
        elif cmd[0:10].lower() == "getupdate ":
            try:
                updateId = int(cmd.split(" ")[1])
            except:
                self._sendInfo("error: {} is not an int".format(cmd.split(" ")[1]))
                return

            info:str = "returnupdate"

            info += " {}".format(Common.updateId)

            tm:Tilemap = Tilemap.tilemaps[0]
            for coord in tm.tiles:
                if tm.tiles[coord].updateID > updateId:
                    info += ' tx{}y{}t{}'.format(coord[0],coord[1],tm.tiles[coord].terrain.intKey)
                    if len(tm.tiles[coord].features)>0:
                        info += 'f{}'.format(','.join(str(feature.intKey) for feature in tm.tiles[coord].features))

            self._sendInfo(info)

        else:
            self._sendInfo("error: cmd unknown at the player level")

    def _sendInfo(self,info):
        '''from PLAYER to PLAYERHELPER'''
        Helper.executeInfo(self,info)


class Helper:
    sendInfoMethod = None 
    mp:Tilemap = None

    def executeCmd(playerId:int,cmd:str):
        '''from GAME to PLAYERHELPER'''

        if cmd.lower() == "createplayer":
            Player(playerId)
        elif cmd.lower() == "deleteplayer":
            del Player._players[playerId]
        else:
            Helper._sendCmd(playerId,cmd)

    def _sendCmd(playerId:int,cmd:str):
        '''from PLAYERHELPER to PLAYER'''
        Player._players[playerId].executeCmd(cmd)

    def executeInfo(sender:Player,info:str):
        '''from PLAYER to PLAYERHELPER
        
        target must be either "ALL", "NONE", or a list of playerID'''
        Helper._sendInfo([sender.playerId],info)

    def _sendInfo(target,info:str):
        '''from PLAYERHELPER to GAME
        
        target must be either "ALL", "NONE", or a list of playerID'''
        if Helper.sendInfoMethod != None:
            Helper.sendInfoMethod(target, info)
        else:
            raise Exception("sendInfoMethod not set")
        