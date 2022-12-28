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
                helptext = "help: list of cmds"
                helptext += "\nclear: clear the console"
                helptext += "\nbindnew: connect on available player id"
                helptext += "\nbind x: connect on player x, where x is a number"
                helptext += "\nunbind: disconnect"
                helptext += "\nquit: stop program"
                helptext += "\nch text: chat text to all players"
                self.rootPanel.consolePrint(helptext)
            elif message == "clear":
                self.rootPanel.consoleClear()
            else:
                self.rootPanel.sendCmd(message)

    def _press_button(self):
        #print("button pressed!")
        self._sendConsoleCmd()

    def enter_pressed(self):
        self._sendConsoleCmd()
