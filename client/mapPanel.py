import tkinter as tk
from PIL import Image,ImageTk

class mapPanel(tk.Frame):
    TILEMAP_PATH = r"./assets/textures/tiles.png"
    TILE_SIZE:int = 32
    '''unit is pixels'''
    SCALE:int = 3
    '''how much to scale up the textures'''


    def __init__(self,parent):
        tk.Frame.__init__(self,parent, relief=tk.SUNKEN, bg = "WHITE")

        self.tileMap = Image.open(mapPanel.TILEMAP_PATH)
        tile = self.tileMap.crop((32,96,64,128))
        self.tkpic = ImageTk.PhotoImage(self.tileMap)
        self.label = tk.Label(self,image=self.tkpic)

        self.SetCameraView((0,0))



    def pack(self):
        tk.Frame.pack(self,expand=True,fill = 'both')
        self.label.pack(expand=True,fill='none',anchor="nw")

    def Draw(self):
        pass

    def _DrawTile(self):
        pass

    def SetTile(self, coordXY,layer:int,spriteIndex:int):
        '''coordXY: [int, int] worldspace position of the tile\n
        layer: 0->terrain, 1->rivers, 2->terrainfeature, 3->ressource, 4->building, 5->roads
        spriteIndex: from 0 to 63, left to right, top to bottom'''
        pass

    def SetCameraView(self, posXY):
        '''posXY: [float, float]'''
        self.posXY = posXY