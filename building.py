import csv
import common

_buildings = {}
class _building:
    def __init__(self, key):
        self.key = key
        self.name = "Unnamed Building"
        self.description = "Default building description."
        self.hammerCost = 50
        self.maintenance = 1
        self.requires = None
        self.obsoletedBy = None
        _buildings[key] = self
        
    @property
    def purchaseCost(self):
        return self.hammerCost*4
    @property
    def sellCost(self):
        return self.hammerCost

    def __repr__(self):
        return "C_BUILDING:{}".format(self.key)


def _loadBuidings():
    with open("buildings.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key = row[0]
                bld = _building(key)
                bld.name = row[1]
                bld.description = row [2]
                bld.hammerCost = row[3]
                bld.maintenance = row[4]
                bld.requires = (None if row[5] == '' else row[5])
                bld.obsoletedBy = (None if row[6] == '' else row[6])
                bld.specials = row[7].split(',')
            


def getBuildables(key_set):
    output = set()
    
    return output

_loadBuidings()