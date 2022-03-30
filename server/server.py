import socket
import threading

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
       
       
    def removeConnectionThread(self, conn):
        # conn.stop()
        self.connectionThreads.remove(conn)

        
    def broadcastInfo(self,info):
        for x in self.connectionThreads:
            x.sendInfo(info)


    
class connectionThread(threading.Thread):
    def __init__(self,server,conn,ip,port):
        self.server = server
        self.conn = conn
        self.ip = ip
        self.port = port
        
        print("[+] Nouveau thread pour {}:{}".format(self.ip, self.port))
        
    def start(self):
        #ask authentification (civkey)
        #receive auth
        self.civkey = "TODO"
        #setup connectionThread
        
        msg = ""
   
        while True:
            try:
                message = self.conn.recv(256)
                if message:
                    self.executeCmd(message)
                else:
                    print("clean disconnect [type 1]")
                    break
            except:
                print("connection interrupted [type 2]")
                break 

    
    def executeCmd(self,cmd):
        print(cmd.decode())
        
    def sendInfo(self, info):
        try:
            conn.send(message)
        except:
            conn.close()
            print("connection interrupted [type 3]")
            remove(conn)

    def stop(self,msg = "No msg"):
        self.conn.close()
        print("[-] Fin du thread pour {}:{}".format(self.ip, self.port))
        server.removeConnectionThread(self)
        
                
if __name__ == "__main__":
    s = server()
    s.start()