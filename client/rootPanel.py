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

        #root>>mainPanel
        self.mainPanel = tk.Frame(self)
        self.mainPanel.config(bg="RED", relief=tk.SUNKEN)
        self.mainPanel.pack(side=tk.LEFT,padx = 5,pady = 5, expand=True,fill = 'both')

        #root>>mainPanel>>mapPanel
        self.mainPanel = mapPanel(self.mainPanel)
        self.mainPanel.pack()
        
        #root>>rightPanel
        self.rightPanel = tk.Frame(self)
        self.rightPanel.config(bg="BLUE", relief=tk.SUNKEN)
        self.rightPanel.pack(side=tk.LEFT,padx = 5,pady = 5, expand=False,fill = 'both')
    
        #root>>rightPanel>>consolePanel
        self.consolePanel = consolePanel(self.rightPanel)
        self.consolePanel.pack()

        #root>>rightPanel>>consoleInputField
        self.consoleInputField = tk.Entry(self.rightPanel)
        self.consoleInputField.bind('<KeyPress>',self.onKeyPress)
        self.consoleInputField.pack(side=tk.LEFT,expand=True, fill = 'x')

        #root>>rightPanel>>consoleInputSendButton
        self.consoleInputSendButton = tk.Button(self.rightPanel, text="envoyer", command=self.press_button)
        self.consoleInputSendButton.pack(side=tk.RIGHT)
        
        
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