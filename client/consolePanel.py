import tkinter as tk

class consolePanel(tk.Message):
    def __init__(self,parent):
        tk.Message.__init__(self,parent,text="", relief=tk.SUNKEN, bg = "WHITE",anchor = tk.NW)
        self.lines = []

    def pack(self):
        tk.Message.pack(self,expand=True, fill='both')

    def print(self,message: str):
        while len(self.lines) >= self.winfo_height()/25:
            self.lines.pop(0)
        self.lines.append(message)
        self.config(text='\n'.join(self.lines))

    def clear(self):
        self.lines = []
        self.config(text = "")