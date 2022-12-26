import tkinter as tk

class ConsoleInput(tk.Entry):
    def __init__(self,parent,rootPanel):
        tk.Frame.__init__(self,parent)
        self.rootPanel=rootPanel

        self.input = tk.Entry(self)
        # self.input.pack(side=tk.LEFT,expand=True, fill = 'x')
        self.input.grid(row=0,column=0)

        self.button = tk.Button(self, text="envoyer", command=self._press_button)
        # self.button.pack(side=tk.RIGHT)
        self.button.grid(row=0,column=1)

    def _sendConsoleCmd(self):
        message = self.input.get()
        if message != "":
            self.input.delete(0,tk.END)
            if message == "help":
                self.rootPanel.consolePrint("""help: list of cmds
                clear: clear the console
                bindnew: connect on available player id
                bind x: connect on player x, where x is a number
                unbind: disconnect
                quit: stop program
                ch text: chat text to all players
                ping: pong
                """)
            elif message == "clear":
                self.rootPanel.consoleClear()
            else:
                self.rootPanel.sendCmd(message)

    def _press_button(self):
        #print("button pressed!")
        self._sendConsoleCmd()

    def enter_pressed(self):
        self._sendConsoleCmd()
