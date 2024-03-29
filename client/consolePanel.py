import tkinter as tk

class ConsolePanel(tk.Message):
    def __init__(self,parent):
        self.fontSize = 8
        self.widthInPixels = 300
        self.widthInChar = int(self.widthInPixels / self.fontSize)-1
        self.rowCount = 20

        tk.Message.__init__(self,parent,text="", relief=tk.SUNKEN, bg = "WHITE",anchor = tk.SW, font=("Courier New", self.fontSize.__str__()),justify="left", width=self.widthInPixels)
        self.lines = []
        self.clear()
        self.focus()

    def print(self,message: str):
        if '\n' in message:
            for x in message.split('\n').__reversed__():
                self.print(x)
        elif len(message) > self.widthInChar:
            self.print(message[self.widthInChar:])
            self.print(message[:self.widthInChar])
        else:
            while len(self.lines) >= self.rowCount:
                self.lines.pop(0)
            self.lines.append(message)
            self.config(text='\n'.join(self.lines.__reversed__()))

    def clear(self):
        #self.lines = []
        #self.config(text = "")
        for _ in range(self.rowCount):
            self.print(".")
