import tkinter as tk

import client
from .mapPanel import mapPanel
from .consolePanel import consolePanel

class rootPanel(tk.Tk):
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
        self.mainPanel = mapPanel(self.mainPanel)
        self.mainPanel.grid(row=0,column=0,sticky='nsew')
        
        #root>>rightPanel
        self.rightPanel = tk.Frame(self)
        self.rightPanel.config(bg="BLUE", relief=tk.SUNKEN)
        self.rightPanel.grid(row=0,column=1,sticky='nsew')
    
        #root>>rightPanel>>consolePanel
        self.consolePanel = consolePanel(self.rightPanel)
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
            self.send_cmd()
        
    def press_button(self):
        print("button pressed!")
        self.send_cmd()

    def send_cmd(self):
        message = self.consoleInputField.get()
        if message != "":
            self.consoleInputField.delete(0,tk.END)
            self.client.sendCmd(message)


            
    def printConsole(self,message: str):
        self.consolePanel.print(message)