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
        self.geometry("800x600")
        self.config(padx = 5,pady = 5)
    
        self.f_main = tk.Frame(self)
        self.f_main.config(bg="RED", relief=tk.SUNKEN)
        self.f_main.pack(side=tk.LEFT,padx = 5,pady = 5, expand=True,fill = 'both')
        
        self.f_details = tk.Frame(self)
        self.f_details.config(bg="BLUE", relief=tk.SUNKEN)
    
        self.m_chatView = tk.Message(self.f_details, text="lorem", relief=tk.SUNKEN, bg = "WHITE")
        self.e_chatEntry = tk.Entry(self.f_details)
        self.b_send = tk.Button(self.f_details, text="envoyer", command=self.press_button)

        self.m_chatView.pack(expand=True, fill='both')
        self.e_chatEntry.pack(side=tk.LEFT,expand=True, fill = 'x')
        self.b_send.pack(side=tk.RIGHT)
        
        self.f_details.pack(side=tk.LEFT,padx = 5,pady = 5, expand=False,fill = 'both')
        
        
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
            self.sendCmd(message)
            
    def printChat(self,message):
        self.m_chatView.config(text=message)

        


        
if __name__ == "__main__":
    app = clientApp()
    app.start()