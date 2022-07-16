import socket
import select

from .mainPanel import mainPanel

class clientApp():
    def __init__(self):
        self.pMain = mainPanel(self)
        self.pMain.protocol("WM_DELETE_WINDOW", self.stop)
        
        self._connect()
        
 
    def _connect(self):
        self.hote = "localhost"
        self.port = 6951
        
        self.ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssocket.connect((self.hote, self.port))
        print ("[+] Connection on {}:{}.".format(self.hote,self.port))
                    
    def stop(self):
        self.quitflag = True
        self.ssocket.close()
        print ("[-] Connection closed.")   
        
        
    def start(self):
        self.quitflag = False

        while True:
            self.pMain.update()
            if self.quitflag:
                break
                
            # self.ssocket.setblocking(0)
            rsock, wsock, esock = select.select([self.ssocket],[],[],0.02)
            for sock in rsock:
                response = sock.recv(256)
                if response != b"":
                    self.executeInfo(response)
  
    def executeInfo(self,encoded_info):
        '''Info must be encoded'''
        print(encoded_info)
        info = encoded_info.decode()

        if info[0:3].lower() == "ch ": #chat
            self.pMain.printChat(info[3:])
        
    def sendCmd(self,cmd):
        self.ssocket.send(cmd.encode())

   
def main():
    app = clientApp()
    app.start()

        
if __name__ == "__main__":
    main()