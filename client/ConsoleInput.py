import tkinter as tk

class ConsoleInput(tk.Entry):
    def __init__(self,parent,rootPanel):
        tk.Frame.__init__(self,parent)
        self.rootPanel=rootPanel

        self.columnconfigure(0, weight= 1, minsize=100)
        self.columnconfigure(1, weight= 0, minsize=50)

        self.input = tk.Entry(self)
        self.input.grid(row=0,column=0,sticky='ew')

        self.button = tk.Button(self, text="envoyer", command=self._press_button)
        self.button.grid(row=0,column=1)

    def _sendConsoleCmd(self):
        message = self.input.get()
        if message != "":
            self.input.delete(0,tk.END)
            if message == "help":
                self.rootPanel.consolePrint("help: list of cmds")
                self.rootPanel.consolePrint("clear: clear the console")
                self.rootPanel.consolePrint("bindnew: connect on available player id")
                self.rootPanel.consolePrint("bind x: connect on player x, where x is a number")
                self.rootPanel.consolePrint("unbind: disconnect")
                self.rootPanel.consolePrint("quit: stop program")
                self.rootPanel.consolePrint("ch text: chat text to all players")
            elif message == "clear":
                self.rootPanel.consoleClear()
            else:
                self.rootPanel.sendCmd(message)

    def _press_button(self):
        #print("button pressed!")
        self._sendConsoleCmd()

    def enter_pressed(self):
        self._sendConsoleCmd()
