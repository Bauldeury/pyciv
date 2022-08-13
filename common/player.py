from common.Tilemap import Tilemap


class player:
    _players = {}

    def __init__(self,playerId):
        if playerId in player._players:
            raise Exception("PlayerID already existing")

        self.playerId = playerId
        player._players[self.playerId] = self

    def __del__(self):
        if self.playerId in player._players: #most of the time no, it's called from the player helper and already deleted
            del player._players[self.playerId]

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
        helper.executeInfo(self,info)


class helper:
    sendInfoMethod = None 
    mp:Tilemap = None

    def executeCmd(playerId:int,cmd:str):
        '''from GAME to PLAYERHELPER'''

        if cmd.lower() == "createplayer":
            player(playerId)
        elif cmd.lower() == "deleteplayer":
            del player._players[playerId]
        else:
            helper._sendCmd(playerId,cmd)

    def _sendCmd(playerId:int,cmd:str):
        '''from PLAYERHELPER to PLAYER'''
        player._players[playerId].executeCmd(cmd)

    def executeInfo(sender:player,info:str):
        '''from PLAYER to PLAYERHELPER
        
        target must be either "ALL", "NONE", or a list of playerID'''
        helper._sendInfo([sender.playerId],info)

    def _sendInfo(target,info:str):
        '''from PLAYERHELPER to GAME
        
        target must be either "ALL", "NONE", or a list of playerID'''
        if helper.sendInfoMethod != None:
            helper.sendInfoMethod(target, info)
        else:
            raise Exception("sendInfoMethod not set")
        