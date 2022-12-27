import tkinter as tk

from client import Client
from .MapPanel import MapPanel
from .ConsolePanel import ConsolePanel
from .ConsoleInput import ConsoleInput

class RootPanel(tk.Tk):
    def __init__(self,client: "Client.Client"):
        tk.Tk.__init__(self)
        
        self.title("Client V2")
        self.client = client
        
        self._initWidgets()
        
    def update(self):
        tk.Tk.update(self)

    def _initWidgets(self):  
        self.geometry("800x600")
        self.config(padx = 5,pady = 5)

        #root
        self.rowconfigure(0,weight=1, minsize= 300)
        self.columnconfigure(0, weight= 3, minsize=300)
        self.columnconfigure(1, weight= 0, minsize=300)
        self.bind('<KeyPress>',self.onKeyPress)

        #root>>mainPanel
        self.mainPanel = tk.Frame(self)
        self.mainPanel.columnconfigure(0,weight= 1)
        self.mainPanel.rowconfigure(0,weight= 1)
        self.mainPanel.config(bg="#ab3030", relief=tk.SUNKEN)
        self.mainPanel.grid(row=0,column=0,sticky='nsew')

        #root>>mainPanel>>mapPanel
        self.mapPanel = MapPanel(self.mainPanel,self)
        self.mapPanel.grid(row=0,column=0,sticky='nsew')
        
        #root>>rightPanel
        self.rightPanel = tk.Frame(self)
        self.rightPanel.config(bg="#3168ac", relief=tk.SUNKEN)
        self.rightPanel.grid(row=0,column=1,sticky='nsew')
    
        #root>>rightPanel>>consolePanel
        self.consolePanel = ConsolePanel(self.rightPanel)
        # self.consolePanel.pack()
        self.consolePanel.grid(row=0,column=0,sticky='ew')

        #root>>rightPanel>>consoleInput
        self.consoleInput = ConsoleInput(self.rightPanel,self)
        self.consoleInput.grid(row=1,column=0,sticky='ew')

    def onKeyPress(self,event):
        # print("Key {} pressed".format(event.char))
        if event.char.lower() == '\r': #key enter
            self.consoleInput.enter_pressed()
  
    def consoleClear(self):
        self.consolePanel.clear()

    def consolePrint(self,txt:str):
        self.consolePanel.print(txt)

    def sendCmd(self, cmd:str):
        self.client.executeCmd(cmd)


    def executeInfo(self,info:str):
        if info[0:3].lower() == "ch ": #chat
            self.consolePanel.print(info[3:])
        elif info[0:13] == "returnupdate ":
            self.mapPanel.Draw()
        elif info[0:13] == "returnbindok ":
            self.mapPanel.Draw()
        elif info == "returnunbindok":
            self.mapPanel.Draw()
