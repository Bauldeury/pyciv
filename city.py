import building
class city:
    
    #ADMIN    
    def __init__(self, name = "Noname"):
        self.population = 1
        self.name = name
        self.foodPile = 0 
        self.buildings = set()
    def __str__(self):
        return "{}: {} pop".format(self.name,self.population)
    def __repr__(self):
        return self.__str__()
        
    def desc(self):
        print("{}: {} pop".format(self.name,self.population))
        fp = self.getFoodProduction()
        if fp > 0:
            print("|{}+{}/{} food".format(self.foodPile,fp,self.getFoodLimit()))
        else:
            print("|{}{}/{} food".format(self.foodPile,fp,self.getFoodLimit()))
        gp = self.getGoldProduction()
        print("|+{} hammers, {}{} gold".format(self.getHammerProduction(),"+" if gp > 0 else "",gp))
        print(self.buildings)
    
    #YIELDS
    def getFoodProduction(self):
        return 3 - self.population + building.getFoodProduction(self.buildings)
    def getHammerProduction(self):
        return 3
    def getGoldProduction(self):
        return self.population
        
    def getFoodLimit(self):
        return self.population * 10
        
    #CONSTRUCTION
    def getBuildables(self):
        return building.getBuildables(self.buildings)
    
    
    #BEHAVIOUR
    def endTurn(self):
        self.foodPile += self.getFoodProduction()
        if self.foodPile < 0 and self.population > 1:
            self.population-=1
            self.foodPile += self.getFoodLimit()
        elif self.foodPile >= self.getFoodLimit():
            self.foodPile -= self.getFoodLimit()
            self.population+=1
