import socket

import common.pyciv
from .connectionThread import *

class server:

    def __init__(self):
        self.connectionThreads = set()
        self.listening = False

        
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
            
            print ("{}:{} opened connection".format(c_ip, c_port))
            
            #open conn
            thread = connectionThread(self,conn,c_ip,c_port)
            self.connectionThreads.add(thread)
            thread.start()
        self.stop()
       
       
    def removeConnectionThread(self, thread):
        # print(self.connectionThreads)
        # print(thread)
        if thread in self.connectionThreads:
            self.connectionThreads.remove(thread)
            # print(self.connectionThreads)

    def executeCmd(self,encoded_cmd):
        '''Cmd must be encoded'''

        cmd = encoded_cmd.decode()
        if cmd[0:3].lower() == "ch ": #chat
            self.broadcastInfo(encoded_cmd)
        
    def broadcastInfo(self,info):
        '''Info must be encoded'''
        for x in self.connectionThreads:
            x.executeInfo(info)


    
      
        
def main():
    s = server()
    s.start()
    
                
if __name__ == "__main__":
    main()