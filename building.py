import csv

class _building:
    def __init__(self):
        self.name = "Unnamed Building"
        self.description = "Default building description."
        self.hammerCost = 50
        self.purchaseCost = 150
        self.maintenance = 1
        self.requires = None
        self.obsoletedBy = None

_dico = {}
_specials = {}


def _loadDictionnary():
    with open("buildings.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                bld = _building()
                bld.name = row[1]
                bld.description = row [2]
                bld.hammerCost = row[3]
                bld.purchaseCost = row[4]
                bld.maintenance = row[5]
                bld.requires = (None if row[6] == '' else row[6])
                bld.obsoletedBy = (None if row[7] == '' else row[7])
                _dico[row[0]] = bld
            
    
def _loadSpecials():
    with open("buildings_specials.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "buildingKey":
                key = row[1]
                values = [row[0]]
                if row[2] != "":
                    values.append(row[2])
                if row[3] != "":
                    values.append(row[3])
                
                _dico[key] = values
            

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