import socket

import common.pyciv
from .connectionThread import *

class server:

    def __init__(self):
        self.connectionThreads = set()
        self.listening = False
        self.players_connectionThread = dict() #key is playerId: int, value is connectionThread
        self.connectionThread_players = dict() #same but reversed because i'm lazy
        
        self.sock = socket.socket()
        host = ""
        port = 6951
        self.sock.bind((host,port))
        
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
        if thread in self.connectionThread_players:
            self.unbindConnectionToPlayer(thread)

        if thread in self.connectionThreads:
            self.connectionThreads.remove(thread)

    def bindConnectionToNewPlayer(self, thread: connectionThread):
        i = 0
        while i in self.players_connectionThread:
            i+=1

        self.bindConnectionToPlayer(thread, i)

    def bindConnectionToPlayer(self, thread: connectionThread, playerId: int):
        if playerId > 255:
            thread.executeInfo(("error: playerId {} out of bounds".format(playerId)).encode())
        elif playerId in self.players_connectionThread:
            thread.executeInfo(("error: playerId {} already binded".format(playerId)).encode())
        elif thread in self.connectionThread_players:
            thread.executeInfo(("error: connection already binded".format(playerId)).encode())
        else:
            self.players_connectionThread[playerId] = thread
            self.connectionThread_players[thread] = playerId
            thread.executeInfo(("playerId {} successfully granted".format(playerId)).encode())

    def unbindConnectionToPlayer(self, thread: connectionThread):
        playerId = self.connectionThread_players[thread]
        del self.players_connectionThread[playerId]
        del self.connectionThread_players[thread]
        thread.executeInfo(("playerId {} successfully revoked".format(playerId)).encode())


    def executeCmd(self,origin: connectionThread,encoded_cmd):
        '''Cmd must be encoded'''

        cmd = encoded_cmd.decode()
        if cmd[0:3].lower() == "ch ": #chat
            print("chat")
            self.broadcastInfo(encoded_cmd)

        elif cmd.lower() == "bindnew": #new player
            self.bindConnectionToNewPlayer(origin)

        elif cmd[0:5].lower() == "bind ": #requesting to connect on a specific number
            id = cmd.split(' ')[1]
            try:
                playerId=int(id)
            except:
                playerId = -1
            if playerId >= 0:
                self.bindConnectionToPlayer(origin,playerId)
            else:
                origin.executeInfo("error: {} is unvalid integer".format(id).encode())

        elif cmd[0:6].lower() == "unbind":
            if origin in self.connectionThread_players:
                self.unbindConnectionToPlayer(origin)
            else:
                origin.executeInfo("error: no playerId to unbind".encode())
                

        else:
            origin.executeInfo("error: cmd unknown".encode())
        
    def broadcastInfo(self,info):
        '''Info must be encoded'''
        for x in self.connectionThreads:
            x.executeInfo(info)


    
      
        
def main():
    s = server()
    s.start()
    
                
if __name__ == "__main__":
    main()