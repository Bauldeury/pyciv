keys = {"PALACE","CASERN", "LIBRARY", "UNIVERSITY", "GRANARY"}
    
# def validateKey(key):
    # if key not in building.keys:
        # raise Exception("ERROR: BuildingKeyUnknown")

def getFoodProduction(key_set):
    output = 0
    if "GRANARY" in key_set:
        output += 5
    return output
    
def getBuildables(key_set):
    output = keys - key_set - {"PALACE"}
    return output
