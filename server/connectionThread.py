import threading
import traceback
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
                print("exception encountered: {}".format(e))
                print(traceback.format_exc())
                print("connection interrupted [type 2]")
                break 
        self.stop()

    
    def executeCmd(self,encoded_cmd):
        '''from CLIENT to CONNECTIONTHREAD
        
        Cmd must be encoded'''
        cmd = encoded_cmd.decode()
        print("{}:{}>>{}".format(self.ip,self.port,cmd))

        if cmd.lower() == "ping":
            self._sendInfo("pong")

        else:
            self._sendCmd(cmd)

    def _sendCmd(self, cmd):
        '''from CONNECTIONTHREAD to SERVER

        targetList must be either "ALL", "NONE", or a list of playerIDs'''
        self.server.executeCmd(self,cmd)

    def executeInfo(self, info:str):
        '''from SERVER to CONNECTIONTHREAD'''
        self._sendInfo(info)
        
    def _sendInfo(self, info:str):
        '''from CONNECTIONTHREAD to CLIENT'''
        print("{}:{}<<{}".format(self.ip,self.port,info))
        encoded_info = info.encode()
        try:
            self.conn.send(encoded_info)
        except:
            self.conn.close()
            print("connection interrupted [type 3]")
            # self.remove(self.conn)

    def stop(self,msg = "No msg"):
        self.conn.close()
        print("[-] Fin du thread pour {}:{}".format(self.ip, self.port))
        self.server.removeConnectionThread(self)
  