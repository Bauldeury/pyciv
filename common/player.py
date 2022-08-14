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
            info:str = "returnupdate"

            tm:Tilemap = Tilemap.tilemaps[0]
            for coord in tm.tiles:
                info += ' tx{}y{}t{}'.format(coord[0],coord[1],tm.tiles[coord].terrain.intKey)
                if tm.tiles[coord].features != None:
                    for fi in tm.tiles[coord].features:
                        info += 'f{}'.format(tm.tiles[coord].features[fi].intKey)

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
        