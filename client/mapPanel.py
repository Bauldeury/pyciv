import tkinter as tk
from PIL import Image,ImageTk

from common import tile
from common import mymap

class mapPanel(tk.Frame):
    TILEMAP_PATH = r"client/assets/tiles.png"
    TILE_SIZE:int = 32
    '''unit is pixels'''


    def __init__(self,parent):
        tk.Frame.__init__(self,parent, relief=tk.SUNKEN, bg = "WHITE")

        self.mymap = mymap.mymap(10,10)
        self.mymap.tiles[(1,1)].addFeature("ROAD")

        self.spriteSheet = Image.open(mapPanel.TILEMAP_PATH)
        self.tkpic = ImageTk.PhotoImage(self.spriteSheet)
        self.label = tk.Label(self)

        self.SetCameraView((0,0))

        self.Draw()


    def pack(self):
        tk.Frame.pack(self,expand=True,fill = 'both')
        self.label.pack(expand=True,fill='none',anchor="nw")

    def Draw(self):
        self.pic = Image.new(mode="RGB",size=(mapPanel.TILE_SIZE*self.mymap.sizeX,mapPanel.TILE_SIZE*self.mymap.sizeY))


        for (x,y) in self.mymap.tiles:
            self._SetTile(self.pic,(x,y),self.mymap.tiles[(x,y)])

        img = self.spriteSheet.crop((32,96,64,128))
        self.tkpic= ImageTk.PhotoImage(self.pic)
        self.label.configure(image=self.tkpic)


    

    def _SetTile(self, image:Image.Image, coordXY,tile:tile.tile):
        '''image: image to draw on\n
        coordXY: [int, int] worldspace position of the tile\n'''
        self._SetSprite(image, coordXY, MapSpriteHelper.TerrainSpriteIndex(tile.terrain.byteKey))  

        if tile.features != None:
            for i in tile.features:
                self._SetSprite(image,coordXY,MapSpriteHelper.FeatureSpriteIndex(tile.features[i].byteKey))


    def _SetSprite(self, image:Image.Image, coordXY,spriteIndex:int):
        '''image: image to draw on\n
        coordXY: [int, int] worldspace position of the tile\n
        spriteIndex: [int, int], left to right, top to bottom'''
        
        tileImage = self.spriteSheet.crop((
            mapPanel.TILE_SIZE * spriteIndex[0],
            mapPanel.TILE_SIZE * spriteIndex[1],
            mapPanel.TILE_SIZE * (spriteIndex[0]+1),
            mapPanel.TILE_SIZE * (spriteIndex[1]+1)
            ))
        image.paste(im=tileImage,box=(coordXY[0]*mapPanel.TILE_SIZE,coordXY[1]*mapPanel.TILE_SIZE),mask=tileImage)


    def SetCameraView(self, posXY):
        '''posXY: [float, float]'''
        self.posXY = posXY

    def MoveCameraView(self, deltaXY):
        '''posXY: [float, float]'''
        self.posXY += deltaXY


class MapSpriteHelper:
    def TerrainSpriteIndex(byteID:int) -> int:
        return (0,0)
    def FeatureSpriteIndex(byteID:int) -> int:
        return (0,2)