import tkinter as tk
from PIL import Image,ImageTk, ImageDraw, ImageFont

from common import tile
from common import mymap

class mapPanel(tk.Frame):
    TILEMAP_PATH = r"client/assets/tiles.png"
    TILE_SIZE:int = 32
    '''unit is pixels'''


    def __init__(self,parent,sendCmd_func):
        tk.Frame.__init__(self,parent, relief=tk.SUNKEN, bg = "WHITE")
        
        self.zoom:int = 2
        self.playerID = None
        self.sendCmd_func = sendCmd_func

        self.mymap = None

        self.xscroll = tk.Scrollbar(self,orient='horizontal')
        self.yscroll = tk.Scrollbar(self,orient='vertical')

        self.spriteSheet = Image.open(mapPanel.TILEMAP_PATH)
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
        elif self.mymap == None:
            self.pic = Image.new(mode='RGB',size=(256,128),color=(0,0,0))
            drawer = ImageDraw.Draw(self.pic)
            myFont = ImageFont.truetype('client/assets/fonts/TitilliumWeb-Regular.ttf', 24)
            drawer.text((2,2),"ERROR:NoMap",font = myFont, fill=(255,0,0))
        else:
            self.pic = Image.new(mode="RGB",size=(mapPanel.TILE_SIZE*self.mymap.sizeX*self.zoom,mapPanel.TILE_SIZE*self.mymap.sizeY*self.zoom))

            for (x,y) in self.mymap.tiles:
                self._SetTile(self.pic,(x,y),self.mymap.tiles[(x,y)])



        self.tkpic= ImageTk.PhotoImage(self.pic)
        # self.canvas.create_image(0,0,image = self.tkpic)
        self.canvas.itemconfig(self.tkpicid,image = self.tkpic)


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
        if self.zoom != 1:
            tileImage = tileImage.resize((mapPanel.TILE_SIZE*self.zoom,mapPanel.TILE_SIZE*self.zoom),resample=Image.NEAREST)
        image.paste(im=tileImage,box=(coordXY[0]*mapPanel.TILE_SIZE*self.zoom,coordXY[1]*mapPanel.TILE_SIZE*self.zoom),mask=tileImage)

    def _onClick(self,event):
        coords = (self.canvas.canvasx(event.x)+self.tkpic.width()/2,self.canvas.canvasy(event.y)+self.tkpic.height()/2)
        # print ("clicked at {},{}".format(int(event.x/(mapPanel.TILE_SIZE*self.zoom)), int(event.y/(mapPanel.TILE_SIZE*self.zoom))))
        coords = tuple(int(i/(mapPanel.TILE_SIZE*self.zoom)) for i in coords)
        print (coords)

        
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
            self.mymap = mymap.mymap(int(x),int(y))
            self.Draw()
            self._refreshScrollers()


    def sendCmd(self,cmd:str):
        self.sendCmd_func(cmd)


class MapSpriteHelper:
    clignot = 0
    def TerrainSpriteIndex(byteID:int) -> int:
        MapSpriteHelper.clignot += 1
        return (MapSpriteHelper.clignot % 3,0)
    def FeatureSpriteIndex(byteID:int) -> int:
        return (0,2)