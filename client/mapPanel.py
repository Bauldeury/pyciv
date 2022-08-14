import tkinter as tk
from PIL import Image,ImageTk, ImageDraw, ImageFont

from common import Tile
from common import Tilemap
from common import Terrain
from common import Feature
from common import Common

class MapPanel(tk.Frame):
    TILEMAP_PATH = r"client/assets/tiles.png"
    TILE_SIZE:int = 32
    '''unit is pixels'''


    def __init__(self,parent,sendCmd_func):
        tk.Frame.__init__(self,parent, relief=tk.SUNKEN, bg = "WHITE")
        
        self.zoom:int = 2
        self.playerID = None
        self.sendCmd_func = sendCmd_func

        self.tilemap = None

        self.xscroll = tk.Scrollbar(self,orient='horizontal')
        self.yscroll = tk.Scrollbar(self,orient='vertical')

        self.spriteSheet = Image.open(MapPanel.TILEMAP_PATH)
        self.canvas = tk.Canvas(self)
        self.tkpicid = self.canvas.create_image(0,0)
        self.Draw()

        self.canvas.grid(row = 0, column = 0,sticky='nsew')
        self.xscroll.grid(row = 1, column = 0,sticky='ew')
        self.yscroll.grid(row = 0, column = 1,sticky='ns')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Set the scrollbars to the canvas
        self.canvas.config(xscrollcommand=self.xscroll.set, 
                           yscrollcommand=self.yscroll.set)
        # Set canvas view to the scrollbars
        self.yscroll.config(command=self.canvas.yview)
        self.xscroll.config(command=self.canvas.xview)

        self._refreshScrollers()


    def mouse_scroll(self, evt):
        #https://stackoverflow.com/questions/56043767/show-large-image-using-scrollbar-in-python
        if evt.state == 0 :
            # self.canvas.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.canvas.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
        if evt.state == 1:
            # self.canvas.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.canvas.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows


    def Draw(self):
        if self.playerID == None:
            self.pic = Image.new(mode='RGB',size=(256,128),color=(0,0,0))
            drawer = ImageDraw.Draw(self.pic)
            myFont = ImageFont.truetype('client/assets/fonts/TitilliumWeb-Regular.ttf', 24)
            drawer.text((2,2),"Unbound",font = myFont, fill=(255,255,255))
        elif self.tilemap == None:
            self.pic = Image.new(mode='RGB',size=(256,128),color=(0,0,0))
            drawer = ImageDraw.Draw(self.pic)
            myFont = ImageFont.truetype('client/assets/fonts/TitilliumWeb-Regular.ttf', 24)
            drawer.text((2,2),"Map loading...",font = myFont, fill=(255,255,0))
        else:
            self.pic = Image.new(mode="RGB",size=(MapPanel.TILE_SIZE*self.tilemap.sizeX*self.zoom,MapPanel.TILE_SIZE*self.tilemap.sizeY*self.zoom))

            for (x,y) in self.tilemap.tiles:
                self._SetTile(self.pic,(x,y),self.tilemap.tiles[(x,y)])



        self.tkpic= ImageTk.PhotoImage(self.pic)
        # self.canvas.create_image(0,0,image = self.tkpic)
        self.canvas.itemconfig(self.tkpicid,image = self.tkpic)


    def _SetTile(self, image:Image.Image, coordXY:"tuple[int,int]",tile:Tile.Tile):
        '''Only called from the draw method
        
        image: image to draw on\n
        coordXY: [int, int] worldspace position of the tile\n'''
        self._SetSprite(image, coordXY, MapSpriteHelper.TerrainSpriteIndex(tile.terrain))  

        if tile.features != None:
            for i in tile.features:
                self._SetSprite(image,coordXY,MapSpriteHelper.FeatureSpriteIndex(tile.features[i]))


    def _SetSprite(self, image:Image.Image, coordXY:"tuple[int,int]",spriteIndex:"tuple[int,int]"):
        '''image: image to draw on\n
        coordXY: tuple[int, int] worldspace position of the tile\n
        spriteIndex: tuple[int, int], left to right, top to bottom'''
        
        tileImage = self.spriteSheet.crop((
            MapPanel.TILE_SIZE * spriteIndex[0],
            MapPanel.TILE_SIZE * spriteIndex[1],
            MapPanel.TILE_SIZE * (spriteIndex[0]+1),
            MapPanel.TILE_SIZE * (spriteIndex[1]+1)
            ))
        if self.zoom != 1:
            tileImage = tileImage.resize((MapPanel.TILE_SIZE*self.zoom,MapPanel.TILE_SIZE*self.zoom),resample=Image.NEAREST)
        image.paste(im=tileImage,box=(coordXY[0]*MapPanel.TILE_SIZE*self.zoom,coordXY[1]*MapPanel.TILE_SIZE*self.zoom),mask=tileImage)

    def _onClick(self,event):
        coords = (self.canvas.canvasx(event.x)+self.tkpic.width()/2,self.canvas.canvasy(event.y)+self.tkpic.height()/2)
        # print ("clicked at {},{}".format(int(event.x/(mapPanel.TILE_SIZE*self.zoom)), int(event.y/(mapPanel.TILE_SIZE*self.zoom))))
        coords = tuple(int(i/(MapPanel.TILE_SIZE*self.zoom)) for i in coords)
        print ("Clicked: {}".format(coords))

        
    def onBind(self,playerID:int):
        self.playerID = playerID
        self.Draw() #too early to draw, don't know the size yet
        self._refreshScrollers()

        #init interaction
        self.canvas.bind("<Button-1>",self._onClick)

        #get initial infos
        self.sendCmd("getmapsize")

    def onUnbind(self):
        self.playerID = None
        self.Draw()
        self._refreshScrollers()

        #unplug interaction
        self.canvas.unbind("<Button-1>")#removes all methods on button1

    def _refreshScrollers(self):
        # Assign the region to be scrolled 
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        #initial scroll
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def executeInfo(self,info:str):
        if info[0:14] == "returnmapsize ":
            _,x,y = info.split(' ')
            self.tilemap = Tilemap.Tilemap(int(x),int(y))
            self.sendCmd("getupdate -1")
        elif info[0:13] == "returnupdate ":
            strings = info.split(' ')
            for string in strings:
                if string[0] == 't': self._updateTileFromString(string)

            self.Draw()
            self._refreshScrollers()



    def sendCmd(self,cmd:str):
        self.sendCmd_func(cmd)

    def _updateTileFromString(self,string:str):
        """reads and works out strings like this: t[x%][y%][u:unexplored][o:fogofwar][t%:terrainID][f%:featureID]"""
        args = Common.decomposeStrToArgs(string[1:],boolArgs=['u','o'],intArgs=['x','y','t'],strArgs=['f'])

        coord = (int(args['x']),int(args['y']))
        tile = Tile.Tile()
        tile.terrain = Terrain.Helper.intToTerrain(int(args["t"]))
        if 'f' in args:
            for f in args['f'].split(','):
                tile.addFeature(Feature.Helper.intToFeature(int(f)).key[0])

        self.tilemap.tiles[coord] = tile


class MapSpriteHelper:
    def TerrainSpriteIndex(terrain:Terrain.Terrain) -> "tuple[int,int]":
        return (terrain.intKey % 8,terrain.intKey // 8)
    def FeatureSpriteIndex(feature:Feature.Feature) -> "tuple[int,int]":
        if feature.key[0] == "ROAD": return (0,4)
        elif feature.key[0] == "RAILROAD": return (0,5)
        else : return (5,7)
    def FogSpriteIndex(): return (6,7)
    def UnexploredSpriteIndex(): return (7,7)