import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont

from common import Tile
from common import Tilemap
from common import Feature
from common import City
from common import Civilization
from client import ArtDefine
from client import DataSynchroniser


class MapPanel(tk.Frame):
    TILEMAP_PATH = r"client/assets/tiles.png"
    TILE_SIZE: int = 32
    """unit is pixels"""

    def __init__(self, parent, rootPanel):
        tk.Frame.__init__(self, parent, relief=tk.SUNKEN, bg="WHITE")

        self.zoom: int = 2
        self.rootPanel = rootPanel

        self.xscroll = tk.Scrollbar(self, orient="horizontal")
        self.yscroll = tk.Scrollbar(self, orient="vertical")

        self.tileSpriteSheet = Image.open(MapPanel.TILEMAP_PATH)
        self.canvas = tk.Canvas(self)
        self.tkpicid = self.canvas.create_image(0, 0)

        self.Draw()

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.xscroll.grid(row=1, column=0, sticky="ew")
        self.yscroll.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Set the scrollbars to the canvas
        self.canvas.config(
            xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set
        )
        # Set canvas view to the scrollbars
        self.yscroll.config(command=self.canvas.yview)
        self.xscroll.config(command=self.canvas.xview)

        self._refreshScrollers()
        self.canvas.bind("<Button-1>", self._onClick)

    def mouse_scroll(self, evt):
        # https://stackoverflow.com/questions/56043767/show-large-image-using-scrollbar-in-python
        if evt.state == 0:
            # self.canvas.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.canvas.yview_scroll(
                int(-1 * (evt.delta / 120)), "units"
            )  # For windows
        if evt.state == 1:
            # self.canvas.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.canvas.xview_scroll(
                int(-1 * (evt.delta / 120)), "units"
            )  # For windows

    def _refreshScrollers(self):
        # Assign the region to be scrolled
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        # initial scroll
        # self.canvas.xview_moveto(0)
        # self.canvas.yview_moveto(0)
            

    def Draw(self):
        if DataSynchroniser.DataSynchroniser.playerId == None:
            self.pic = Image.new(mode="RGB", size=(256, 128), color=(0, 0, 0))
            drawer = ImageDraw.Draw(self.pic)
            myFont = ImageFont.truetype(
                "client/assets/fonts/TitilliumWeb-Regular.ttf", 24
            )
            drawer.text((2, 2), "Unbound", font=myFont, fill=(255, 255, 255))

        elif 0 not in Tilemap.tilemaps:
            self.pic = Image.new(mode="RGB", size=(256, 128), color=(0, 0, 0))
            drawer = ImageDraw.Draw(self.pic)
            myFont = ImageFont.truetype(
                "client/assets/fonts/TitilliumWeb-Regular.ttf", 24
            )
            drawer.text((2, 2), "Map loading...", font=myFont, fill=(255, 255, 0))

        else:
            self.pic = Image.new(
                mode="RGB",
                size=(
                    MapPanel.TILE_SIZE * Tilemap.tilemaps[0].sizeX * self.zoom,
                    MapPanel.TILE_SIZE * Tilemap.tilemaps[0].sizeY * self.zoom,
                ),
            )
            for (x, y) in Tilemap.tilemaps[0].tiles:
                self._SetTile(self.pic, (x, y), Tilemap.tilemaps[0].tiles[(x, y)])
            for city in City.City.cities.values():
                self._SetCity(self.pic, city)

        self.tkpic = ImageTk.PhotoImage(self.pic)
        # self.canvas.create_image(0,0,image = self.tkpic)
        self.canvas.itemconfig(self.tkpicid, image=self.tkpic)
        self._refreshScrollers()
        

    def _SetTile(self, image: Image.Image, coordXY: "tuple[int,int]", tile: Tile.Tile):
        """Only called from the draw method

        image: image to draw on\n
        coordXY: [int, int] worldspace position of the tile\n"""
        self._SetSprite(image, coordXY, ArtDefine.tileArtDefines[tile.terrain.key].xy)

        if tile.features != None:
            for feature in tile.features:
                self._SetSprite(
                    image, coordXY, ArtDefine.tileArtDefines[feature.key].xy
                )

                
    def _SetCity(self, image: Image.Image, city:City.City):
        """Only called from the draw method

        image: image to draw on\n
        city: city to draw\n"""
        self._SetSprite(image, city.pos, ArtDefine.tileArtDefines["CITY"].xy)
        #self._BorderTile(image, city.pos, Civilization.Helper.getcivilization(city.owner).color)
        self._BorderTile(image, city.pos, "#0000ff")

    def _SetSprite(
        self,
        image: Image.Image,
        coordXY: "tuple[int,int]",
        spriteIndex: "tuple[int,int]",
    ):
        """image: image to draw on\n
        coordXY: tuple[int, int] worldspace position of the tile\n
        spriteIndex: tuple[int, int], left to right, top to bottom"""

        tileImage = self.tileSpriteSheet.crop(
            (
                MapPanel.TILE_SIZE * spriteIndex[0],
                MapPanel.TILE_SIZE * spriteIndex[1],
                MapPanel.TILE_SIZE * (spriteIndex[0] + 1),
                MapPanel.TILE_SIZE * (spriteIndex[1] + 1),
            )
        )
        if self.zoom != 1:
            tileImage = tileImage.resize(
                (MapPanel.TILE_SIZE * self.zoom, MapPanel.TILE_SIZE * self.zoom),
                resample=Image.NEAREST,
            )
        image.paste(
            im=tileImage,
            box=(
                coordXY[0] * MapPanel.TILE_SIZE * self.zoom,
                coordXY[1] * MapPanel.TILE_SIZE * self.zoom,
            ),
            mask=tileImage,
        )

    def _BorderTile(
        self,
        image: Image.Image,
        coordXY: "tuple[int,int]",
        color
        ):
        """image: image to draw on\n
        coordXY: tuple[int, int] worldspace position of the tile\n
        color: '#112233', color of the border"""
        drawer = ImageDraw.Draw(image)
        x1 = (coordXY[0] * MapPanel.TILE_SIZE+1) * self.zoom
        y1 = (coordXY[1] * MapPanel.TILE_SIZE+1) * self.zoom
        x2 = ((coordXY[0]+1) * MapPanel.TILE_SIZE-1) * self.zoom
        y2 = ((coordXY[1] +1)* MapPanel.TILE_SIZE-1) * self.zoom
        drawer.line([(x1,y1),(x2,y1)],fill=color, width=self.zoom)
        drawer.line([(x2,y2),(x2,y1)],fill=color, width=self.zoom)
        drawer.line([(x2,y2),(x1,y2)],fill=color, width=self.zoom)
        drawer.line([(x1,y1),(x1,y2)],fill=color, width=self.zoom)


    def _onClick(self, event):
        coords = (
            self.canvas.canvasx(event.x) + self.tkpic.width() / 2,
            self.canvas.canvasy(event.y) + self.tkpic.height() / 2,
        )
        # print ("clicked at {},{}".format(int(event.x/(mapPanel.TILE_SIZE*self.zoom)), int(event.y/(mapPanel.TILE_SIZE*self.zoom))))
        coords = tuple(int(i / (MapPanel.TILE_SIZE * self.zoom)) for i in coords)
        #print("Clicked: {}".format(coords))
        if 0 in Tilemap.tilemaps:
            tile:Tile.Tile = Tilemap.tilemaps[0].getTile(coords)
            if tile != None:
                text = "{} {}".format(coords, tile.terrain.name)
                for f in tile.features:
                    text += ",{}".format(f.name)
                city:City.City = City.Helper.getCityOnPos(coords)
                if city != None:
                    text += "\n{}(owner:{})".format(city.name,city.owner)
                text += "\n--------"
                self.rootPanel.consolePrint(text)
