import socket
import select
import tkinter as tk

class clientApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Client V2")
        
        # self.bind('<Escape>',self.stop)
        self.protocol("WM_DELETE_WINDOW", self.stop)
        
        self._initWidgets()
        self._connect()
        

    def _initWidgets(self):  
        self.geometry("400x300")
        self.config(padx = 15,pady = 10)
    
        self.m_chatView = tk.Message(self, text="lorem", relief=tk.SUNKEN, bg = "WHITE")
        self.e_chatEntry = tk.Entry(self)
        self.b_send = tk.Button(self, text="envoyer", command=self.press_button)

        self.m_chatView.pack(expand=True, fill='both')
        self.e_chatEntry.pack(side=tk.LEFT,expand=True, fill = 'x')
        self.b_send.pack(side=tk.RIGHT)
        
        
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
            self.update()
            if self.quitflag:
                break
                
            # self.ssocket.setblocking(0)
            rsock, wsock, esock = select.select([self.ssocket],[],[],0.02)
            for sock in rsock:
                response = sock.recv(256).decode()
                if response != b"":
                    executeInfo(response)
  
    def executeInfo(self,info):
        print(info)
        self.printChat(info)
        
    def sendCmd(self,cmd):
        self.ssocket.send(cmd.encode())
        
        
    def press_button(self):
        print("button pressed!")
        message = self.e_chatEntry.get()
        if message != "":
            self.e_chatEntry.delete(0,tk.END)
            sendCmd(message)
            
    def printChat(self,message):
        self.m_chatView.config(text=message)

        


        
if __name__ == "__main__":
    app = clientApp()
    app.start()