class server:
    def __init__(self):
        self.players = set()
        self.listening = False
        
    def start(self):
        self.listening = True
        self.listenForConnection()
    
    def stop(self):
        self.listening = False
        for x in self.players:
            x.stop()
        
    def __del__(self):
        self.stop()
        
    def listenForConnection(self):
        while self.listening:
            break
            #listen conn
            #open conn
            conn = playerConnection(self)
            addConnection(conn)
            
        pass
        
    def addConnection(self, conn):
        self.players.add(conn)
        conn.start()
    
    def removeConnection(self, conn):
        conn.stop()
        self.players.remove(conn)

        
    def broadcastInfo(self,info):
        for x in self.players:
            x.sendInfo(info)


    
class playerConnection:
    def __init__(self,server):
        self.server = server
        
    def start(self):
        #ask authentification (civkey)
        #receive auth
        self.civkey = "TODO"
        #setup playerConnection
        #setup thread
        pass
    
    def stop(self):
        pass
        
    def stopCmd(self):
        server.removeConnection(self)
        
    def listenCmd(self):
        pass
    
    def executeCmd(self,cmd):
        pass
        
    def sendInfo(self, info):
        pass