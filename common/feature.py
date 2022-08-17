import csv

from . import Common

features:"dict[str,Feature]" = {}
class Feature:
    def __init__(self,key):
        self.key:str = key
        self.intKey:int = len(features)
        self.name:str = "FeatureName"
        self.description:str = "FeatureDescription"
        self.requiresTech:str = None
        self.constraints:"list[str]" = []
        self.workAmount:int = 0
        self.specials:"list[str]" = []
        self.tags:"list[str]" = []
        features[self.key] = self
    
    def __repr__(self):
        return "C_FEATURE:{}".format(self.key)

def _loadFeatures():
    with open(Common.getCommonPath()+"features.csv", newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                cKey = row.index("key")
                cName = row.index("name")
                cDescription = row.index("description")
                cRequiresTech = row.index("requiresTech")
                cConstraints = row.index("constraints")
                cWorkAmount = row.index("workAmount")
                cSpecials = row.index("specials")
                cTags = row.index("tags")
            else:
                key = row[cKey]
                f = Feature(key)

                f.name = row[cName]
                f.description = row[cDescription]
                f.requiresTech = row[cRequiresTech] if row[cRequiresTech] != "" else None
                f.constraints = row[cConstraints].split(',') if row[cConstraints] != "" else []
                f.workAmount = int(row[cWorkAmount]) if row[cWorkAmount] != "" else 0
                f.specials = row[cSpecials].split(',') if row[cSpecials] != "" else []
                f.tags = row[cTags].split(',') if row[cTags] != "" else []

class Helper:
    def intToFeature(intKey:int)->"Feature|None":
        for item in features.values():
            if item.intKey == intKey:
                return item
        return None
    
                   
_loadFeatures()