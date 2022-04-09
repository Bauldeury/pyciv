import tkinter as tk
import client

class mainPanel(tk.Tk):
    def __init__(self,client):
        tk.Tk.__init__(self)
        
        self.title("Client V2")
        self.client = client
        
        self._initWidgets()
        
    def update(self):
        tk.Tk.update(self)

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
        
                
        
    def press_button(self):
        print("button pressed!")
        message = self.e_chatEntry.get()
        if message != "":
            self.e_chatEntry.delete(0,tk.END)
            self.client.sendCmd(message)
            
    def printChat(self,message):
        self.m_chatView.config(text=message)