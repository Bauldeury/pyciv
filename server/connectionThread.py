import threading
import server

class connectionThread(threading.Thread):
    def __init__(self,server,conn,ip,port):
        threading.Thread.__init__(self)
        self.server: server = server
        self.conn = conn
        self.ip = ip
        self.port = port
        
        print("[+] Nouveau thread pour {}:{}".format(self.ip, self.port))
        
    def run(self):
        msg = ""
   
        while True:
            try:
                message = self.conn.recv(256)
                if message:
                    self.executeCmd(message)
                else:
                    print("clean disconnect [type 1]")
                    break
            except Exception as e:
                print(e)
                print("connection interrupted [type 2]")
                break 
        self.stop()

    
    def executeCmd(self,encoded_cmd):
        '''Cmd must be encoded'''
        cmd = encoded_cmd.decode()
        print("{}:{}>>{}".format(self.ip,self.port,cmd))

        if cmd.lower() == "ping":
            print("{}:{}<<ponging back".format(self.ip,self.port))
            self.sendInfo("pong".encode())

        elif cmd[0:3].lower() == "ch ": #chat
            self.broadcastCmd(encoded_cmd)

        else:
            self.server.executeCmd(self, encoded_cmd)

    def executeInfo(self, info):
        '''info must be encoded'''
        self.sendInfo(info)
        
    def sendInfo(self, info):
        '''info must be encoded'''
        try:
            self.conn.send(info)
        except:
            self.conn.close()
            print("connection interrupted [type 3]")
            # self.remove(self.conn)

    def broadcastCmd(self,cmd):
        '''Cmd must be encoded'''
        self.server.executeCmd(self,cmd)

    def stop(self,msg = "No msg"):
        self.conn.close()
        print("[-] Fin du thread pour {}:{}".format(self.ip, self.port))
        self.server.removeConnectionThread(self)
  