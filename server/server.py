import socket
from sqlite3 import connect

from common.game import game
from .connectionThread import *

class server:

    def __init__(self):
        self.connectionThreads:set[connectionThread] = set()
        self.listening = False
        
        self.sock = socket.socket()
        host = ""
        port = 6951
        self.sock.bind((host,port))

        self.game = game()
        self.game.sendInfoMethod = self.executeInfo
        
    def start(self):
        self.listening = True
        self._listenForConnection()
    
    def stop(self):
        self.listening = False
        for x in self.connectionThreads:
            x.stop()
        self.sock.close()
        
    def __del__(self):
        self.stop()
        
        
    def _listenForConnection(self):
        while self.listening:
            self.sock.listen(5)
            (conn, (c_ip, c_port)) = self.sock.accept()
            self.createConnectionThread(conn, c_ip, c_port)
            
        self.stop()
       
    def createConnectionThread(self, conn, c_ip, c_port):
        print ("{}:{} opened connection".format(c_ip, c_port))
        #open conn
        thread = connectionThread(self,conn,c_ip,c_port)
        self.connectionThreads.add(thread)
        thread.start()
       
    def removeConnectionThread(self, thread: connectionThread):
        if thread.playerID != None:
            self.unbindConnectionToPlayer(thread)

        if thread in self.connectionThreads:
            self.connectionThreads.remove(thread)

    def _playerIDtoThread(self, playerID: int):
        '''returns the thread or -None- if not found'''
        for thread in self.connectionThreads:
            if thread.playerID == playerID:
                return thread
        return None


    def bindConnectionToNewPlayer(self, thread: connectionThread):
        i = 0
        while self._playerIDtoThread(i) != None:
            i+=1

        self.bindConnectionToPlayer(thread, i)

    def bindConnectionToPlayer(self, thread: connectionThread, playerId: int):
        if self._playerIDtoThread(playerId) != None:
            thread.executeInfo(("error: playerId {} already bound".format(playerId)))
        elif thread.playerID != None:
            thread.executeInfo(("error: thread already bound".format(playerId)))
        else:
            self._sendCmd(playerId,"createplayer")
            thread.playerID = playerId
            thread.playerName = "player#{}".format(playerId)
            thread.executeInfo("returnbindok {}".format(playerId))

    def unbindConnectionToPlayer(self, thread: connectionThread):
        playerId = thread.playerID
        self._sendCmd(playerId,"deleteplayer")
        thread.playerID = None
        thread.playerName = "UT"
        thread.executeInfo("returnunbindok")


    def executeCmd(self,sender: connectionThread,cmd:str):
        '''From THREAD to SERVER'''

        if cmd[0:3].lower() == "ch ": #chat
            self._sendInfo("ALL","ch " + sender.playerName + ": " + cmd[3:])

        elif cmd.lower() == "bindnew": #new player
            self.bindConnectionToNewPlayer(sender)

        elif cmd[0:5].lower() == "bind ": #requesting to connect on a specific number
            id = cmd.split(' ')[1]
            try:
                playerId=int(id)
            except:
                playerId = -1
            if playerId >= 0:
                self.bindConnectionToPlayer(sender,playerId)
            else:
                sender.executeInfo("error: {} is unvalid integer".format(id))

        elif cmd.lower() == "getbind":
            self._sendInfo({sender},"returnbind {}".format(sender.playerID))

        elif cmd.lower() == "unbind":
            if sender.playerID != None:
                self.unbindConnectionToPlayer(sender)
            else:
                sender.executeInfo("error: no playerId to unbind")

        elif cmd[0:12].lower() == "createplayer":
            sender.executeInfo("error: forbidden command")
        elif cmd[0:12].lower() == "deleteplayer":
            sender.executeInfo("error: forbidden command")

        else:
            if sender.playerID != None:
                self._sendCmd(sender.playerID,cmd)
            else:
                sender.executeInfo("error: cmd not understood at the server level")

    
    def _sendCmd(self,sender: int, cmd:str):
        '''From SERVER to GAME'''
        self.game.executeCmd(sender,cmd)

    def executeInfo(self,target,info:str):
        '''From GAME to SERVER

        target must be either "ALL", "NONE", or a list of playerID'''

        if target == "ALL" or target == "NONE":
            self._sendInfo(target,info)
        else:
            threads = []
            for playerId in target:
                threads.append(self._playerIDtoThread(playerId))
            self._sendInfo(threads,info)

    def _sendInfo(self,target,info:str):
        '''From SERVER to THREAD(s)

        target must be either "ALL", "NONE", or a list of connectionThread'''
        if target == "ALL":
            for x in self.connectionThreads:
                x.executeInfo(info)
        elif target == "NONE":
            return
        else:
            for x in target:
                x.executeInfo(info)
        


    
      
        
def main():
    s = server()
    s.start()
    
                
if __name__ == "__main__":
    main()