import math

from . import tile
    

class mymap:
    def __init__(self,sizeX,sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.tiles:dict[str,tile.tile]= {}
        for x in range (sizeX):
            for y in range (sizeY):
                self.tiles[(x,y)] = tile.tile()
               
    def getTile(self,pos):
        if self.isPosValid(pos):
            return self.tiles[pos]
        else:
            return None
            
    def isPosValid(self,pos):
        if pos[0] >= self.sizeX or pos[1] >= self.sizeY or pos[0] < 0 or pos[1] <0:
            return False
        return True
        
    def getTravelCost(self, pos1, pos2):
        if helper.chebyshevDistance(pos1,pos2) != 1:
            return None
        else:
            return max(self.getTile[pos1].travelCost,self.getTile[pos2].travelCost)
        
            
class helper:
    def offsetN(pos):
        return (pos[0],pos[1]+1)
    def offsetS(pos):
        return (pos[0],pos[1]-1)
    def offsetW(pos):
        return (pos[0]-1,pos[1])
    def offsetE(pos):
        return (pos[0]+1,pos[1])
        
    def offsetNW(pos):
        return (pos[0]-1,pos[1]+1)
    def offsetNE(pos):
        return (pos[0]+1,pos[1]+1)
    def offsetSW(pos):
        return (pos[0]-1,pos[1]-1)
    def offsetSE(pos):
        return (pos[0]+1,pos[1]-1)
        
    def posNeighboors(pos):
        return [helper.offsetN(pos),helper.offsetNE(pos),helper.offsetE(pos),helper.offsetSE(pos),helper.offsetS(pos),helper.offsetSW(pos),helper.offsetW(pos),helper.offsetNW(pos)]
            
    def euclidianDistance(pos1,pos2):
        return math.sqrt(abs(pos1[0]-pos2[0])**2+abs(pos1[1]-pos2[1])**2)
    def manhattanDistance(pos1,pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])
    def chebyshevDistance(pos1,pos2):
        return max(abs(pos1[0]-pos2[0]),abs(pos1[1]-pos2[1]))
       


