import building
import civilization

_cities = {}
class city:
    _citiesNextKey = 0
    
    #ADMIN    
    def __init__(self, tile, name = "Noname", owner = None):
        self.key = city._citiesNextKey
        city._citiesNextKey += 1
        _cities[self.key] = self
        
        self.name = name
        self.owner = owner
        self.tile = tile
        
        self.population = 1
        self.foodPile = 0 
        
        self.buildings = building.buildingSet(city = self)
        
        self._properties = dict()
        self._computeFlag = True
        self._computeProperties()

        
    def __repr__(self):
        return "C_CITY:({},{})".format(self.key,self.name)
        
    def desc(self):
        print("{}: {} pop".format(self.name,self.population))
        print("|{}{:+}/{} food".format(self.foodPile,self.foodYield,self.foodLimit))
        print("|{:+} prod., {:+} comm.".format(self.productionYield,self.commerceYield))
        print(self.buildings)
    
    #PROPERTIES
    def _computeProperties(self):
        if self._computeFlag == False:
            return
        self._computeFlag = False 
        
        #population growth computation
        self._properties["POP_SUPPORT"] = 5 + self.buildings.special("POP_SUPPORT")
        self._properties["FOOD_YIELD"] = 3 - self.population*2 + self.buildings.special("FOOD_YIELD")
        
        #other computations
        self._properties["PRODUCTION_YIELD"] = 3 + self.buildings.special("PRODUCTION_YIELD")
        self._properties["COMMERCE_YIELD"] = self.population + self.buildings.special("COMMERCE_YIELD")
        
    
    @property
    def foodYield(self):
        return self._properties["FOOD_YIELD"]
    @property
    def productionYield(self):
        return self._properties["PRODUCTION_YIELD"]
    @property
    def commerceYield(self):
        return self._properties["COMMERCE_YIELD"]
    @property
    def foodLimit(self):
        return self.population * 10
    @property
    def popSupport(self):
        return self._properties["POP_SUPPORT"]
        
    #CONSTRUCTION
    def getBuildables(self):
        return self.buildings.getBuildables()
    
    
    #BEHAVIOUR
    def endTurn(self):
        self._computeProperties()
    
        #pop evolution
        self.foodPile += self.foodYield
        
        #pop shrink
        if self.foodPile < 0 and self.population > 1:
            self.population-=1
            self.foodPile += self.foodLimit
            self._computeFlag = True
            
        #pop growth  
        elif self.foodPile >= self.foodLimit:
            if self.population >= self.popSupport:#pop limit reached
                self.foodPile = self.foodLimit
            else:#pop limit not reached
                self.foodPile -= self.foodLimit
                self.population+=1
                self._computeFlag = True
            
            
            
        self._computeProperties()

class helper():
    def endTurn():
        for i_city in _cities:
            _cities[i_city].endTurn()
