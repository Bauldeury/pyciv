class _building:
    def __init__(self):
        self.name = "Unnamed Building"
        self.hammerCost = 50
        self.purchaseCost = 150
        self.maintenance = 1
        self.requires = None
        self.obsoletedBy = None

#keys = {"AQUEDUCT","BANK","BARRACKS","CATHEDRAL","CITY WALLS","COLOSSEUM","COURTHOUSE","FACTORY","GRANARY","HYDRO PLANT", "LIBRARY", "MARKETPLACE","MASS TRANSIT","MFG PLANT", "NUCLEAR PLANT", "PALACE", "POWER PLANT", "RECYCLING CENTER", "SDI DEFENSE","TEMPLE","UNIVERSITY"}
_dico = {}


def _loadDictionnary():

    barracks = _building()
    barracks.name = "barracks"
    barracks.hammerCost = 40
    barracks.purchaseCost = 160
    barracks.maintenance = 0
    _dico["BARRACKS"] = barracks
    
def _loadSpecials():
    pass

def getFoodProduction(key_set):
    output = 0
    if "GRANARY" in key_set:
        output += 5
    return output
    
def getGoldProduction(key_set):
    #maintenance of the buildings
    output = 0
    return output
    
def getBuildables(key_set):
    output = set()
    
    return output

_loadDictionnary()
_loadSpecials()