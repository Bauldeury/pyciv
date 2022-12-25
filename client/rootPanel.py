import tkinter as tk

from client import Client
from .MapPanel import MapPanel
from .ConsolePanel import ConsolePanel

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
            # print("enter pressed!")
            self._sendConsoleCmd()
        
    def press_button(self):
        print("button pressed!")
        self._sendConsoleCmd()

    def _sendConsoleCmd(self):
        message = self.consoleInputField.get()
        if message != "":
            self.consoleInputField.delete(0,tk.END)
            if message == "help":
                self.consolePanel.print("""help: list of cmds
                clear: clear the console
                bindnew: connect on available player id
                bind x: connect on player x, where x is a number
                unbind: disconnect
                quit: stop program
                ch text: chat text to all players
                ping: pong
                """)
            elif message == "clear":
                self.consolePanel.clear()
            else:
                self.sendCmd(message)

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
