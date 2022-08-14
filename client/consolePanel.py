import tkinter as tk

class ConsolePanel(tk.Message):
    def __init__(self,parent):
        tk.Message.__init__(self,parent,text="", relief=tk.SUNKEN, bg = "WHITE",anchor = tk.NW)
        self.lines = []

    def print(self,message: str):
        while len(self.lines) >= 5:
            self.lines.pop(0)
        self.lines.append(message)
        self.config(text='\n'.join(self.lines))

    def clear(self):
        self.lines = []
        self.config(text = "")