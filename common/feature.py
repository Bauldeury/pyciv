import csv

from . import common

features = {}
class feature:
    def __init__(self,key):
        self.key = key
        self.byteKey = int.to_bytes(len(features),length=1,byteorder='big')
        self.name = "FeatureName"
        self.description = "FeatureDescription"
        self.requires = None
        self.constraints = None
        self.ftype = 0 #0 for natural features, 1 for resources, 2 for roads, 3 for other improvements
        self.workAmount = 50
        self.specials = None
        features[self.key] = self
    
    def __repr__(self):
        return "C_FEATURE:{}".format(self.key)

def _loadFeatures():
    with open(common.getCommonPath()+"features.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] != "key":
                key =(row[0],row[1] if row[1]!="" else None)
                f = feature(key)
                
                f.name = row[2]
                f.description = row[3]
                f.requires = row[4] if row[4] != "" else None
                f.constraints = row[5].split(',') if row[5] != "" else None
                f.ftype = int(row[6]) #0 for natural features, 1 for resources, 2 for roads, 3 for other improvements
                f.workAmount = int(row[7]) if row[7] != "" else None
                f.specials = row[8].split(',') if row[8] != "" else None

class helper:
    def byteToFeature(byteKey):
        for item in features.values():
            if item.byteKey == byteKey:
                return item
        return None
    
                   
_loadFeatures()