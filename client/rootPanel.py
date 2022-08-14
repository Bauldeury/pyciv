import tkinter as tk

from .MapPanel import MapPanel
from .ConsolePanel import ConsolePanel

class RootPanel(tk.Tk):
    def __init__(self,client):
        tk.Tk.__init__(self)
        
        self.title("Client V2")
        self.client = client
        self.playerId = None
        
        self._initWidgets()
        
    def update(self):
        tk.Tk.update(self)

    def _initWidgets(self):  
        self.geometry("800x600")
        self.config(padx = 5,pady = 5)

        #root
        self.rowconfigure(0,weight=1, minsize= 300)
        self.columnconfigure(0, weight= 3, minsize=300)
        self.columnconfigure(1, weight= 1, minsize=100)

        #root>>mainPanel
        self.mainPanel = tk.Frame(self)
        self.mainPanel.columnconfigure(0,weight= 1)
        self.mainPanel.rowconfigure(0,weight= 1)
        self.mainPanel.config(bg="RED", relief=tk.SUNKEN)
        self.mainPanel.grid(row=0,column=0,sticky='nsew')

        #root>>mainPanel>>mapPanel
        self.mapPanel = MapPanel(self.mainPanel,self.sendCmd)
        self.mapPanel.grid(row=0,column=0,sticky='nsew')
        
        #root>>rightPanel
        self.rightPanel = tk.Frame(self)
        self.rightPanel.config(bg="BLUE", relief=tk.SUNKEN)
        self.rightPanel.grid(row=0,column=1,sticky='nsew')
    
        #root>>rightPanel>>consolePanel
        self.consolePanel = ConsolePanel(self.rightPanel)
        # self.consolePanel.pack()
        self.consolePanel.grid(row=0,column=0,sticky='ew')


        #root>>rightPanel>>consoleInput
        self.consoleInput = tk.Frame(self.rightPanel)
        self.consoleInput.grid(row=1,column=0,sticky='ew')

        #root>>rightPanel>>consoleInput>>consoleInputField
        self.consoleInputField = tk.Entry(self.consoleInput)
        self.consoleInputField.bind('<KeyPress>',self.onKeyPress)
        # self.consoleInputField.pack(side=tk.LEFT,expand=True, fill = 'x')
        self.consoleInputField.grid(row=0,column=0)

        #root>>rightPanel>>consoleInput>>consoleInputSendButton
        self.consoleInputSendButton = tk.Button(self.consoleInput, text="envoyer", command=self.press_button)
        # self.consoleInputSendButton.pack(side=tk.RIGHT)
        self.consoleInputSendButton.grid(row=0,column=1)
        
        
    def onKeyPress(self,event):
        # print("Key {} pressed".format(event.char))
        if event.char.lower() == '\r': #key enter
            print("enter pressed!")
            self._sendConsoleCmd()
        
    def press_button(self):
        print("button pressed!")
        self._sendConsoleCmd()

    def _sendConsoleCmd(self):
        message = self.consoleInputField.get()
        if message != "":
            self.consoleInputField.delete(0,tk.END)
            self.sendCmd(message)

    def sendCmd(self, cmd:str):
        self.client.sendCmd(cmd)


    def executeInfo(self,info:str):
        if info[0:3].lower() == "ch ": #chat
            self.consolePanel.print(info[3:])
        elif info[0:13] == "returnbindok ":
            self._onBind(info.split(' ')[1])
        elif info == "returnunbindok":
            self._onUnbind()
        elif info[0:14] == "returnmapsize ":
            self.mapPanel.executeInfo(info)
        elif info[0:13] == "returnupdate ":
            self.mapPanel.executeInfo(info)

    def _onBind(self,playerID:int):
        self.playerId = playerID
        self.mapPanel.onBind(playerID)

    def _onUnbind(self):
        self.playerId = None
        self.mapPanel.onUnbind()