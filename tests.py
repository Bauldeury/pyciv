import map
import city
import building
import unit

import csv

def printInstance(ins):
    print('\n'.join("{}:{}".format(k,v) for k,v in ins.__dict__.items()))
    
def indentedPrint(txt = ""):
    print("|_ {}".format(txt))

# mymap = map.map(10,10)

# print()
# print("TERRAIN TEST: DESERT")
# t = map._terrains["DESERT"]
# printInstance(t)
# del t

# print()
# print("FEATURE TEST: RAILROAD")
# f = map._features[("RAILROAD","DESERT")]
# printInstance(f)
# del f

# print()
# print("TILE TEST: PLAINS, WHEAT, ROAD then overwrite with RAILROAD")
# t = map.tile()
# t.terrain = map._terrains["PLAINS"]
# t.addFeature("WHEAT")
# t.addFeature("ROAD")
# t.addFeature("RAILROAD")
# printInstance(t)
# del t

# print()
# print("YIELD TEST: PLAINS, WHEAT, IRRIGATION,RAILROAD")
# t = map.tile()
# t.addFeature("WHEAT")
# t.addFeature("IRRIGATION")
# t.addFeature("RAILROAD")
# print("FOOD:{}".format(t.foodYield))
# print("TRAVEL_COST:{}".format(t.travelCost))
# del t

def testTileComputation(verbose):
    #init
    if verbose:
        indentedPrint("testTileComputation START")
        indentedPrint()
    out_messages = []

    #basic data
    tr = map._terrain()
    tr.key = "TR_TEST"
    tr.foodYield = 3
    tr.productionYield = 2
    tr.commerceYield = 1
    tr.travelCost = 1
    tr.defensiveBonus = 0
    map._terrains[tr.key] = tr
    if verbose:
        indentedPrint(tr)
        indentedPrint("FOOD:{}, PROD:{}, COMM:{}, MOVE:{}, DEF:{}".format(tr.foodYield,tr.productionYield,tr.commerceYield,tr.travelCost, tr.defensiveBonus) )
        indentedPrint()
    
    ft = map._feature()
    ft.key = ("FT_TEST","TR_TEST")
    ft.specials = ["COMMERCE_YIELD","4","DEFENSIVE_BONUS","100","SET_MOVEMENT_COST","0.5","ALL_MULTIPLIER","1.5"]
    map._features[ft.key] = ft
    if verbose:
        indentedPrint(ft)
        indentedPrint(ft.specials)
        indentedPrint()
    
    t = map.tile()
    t.terrain = map._terrains["TR_TEST"]
    
    #test 1 : bare terrain
    testString = "FOOD:{}, PROD:{}, COMM:{}, MOVE:{}, DEF:{}".format(t.foodYield,t.productionYield,t.commerceYield,t.travelCost, t.defensiveBonus)
    target = "FOOD:3, PROD:2, COMM:1, MOVE:1, DEF:0"
    error = target != testString
    if error :
        message = "ERROR: base terrain computation failed"
        out_messages.append(message)
    if verbose:
        indentedPrint(t)
        indentedPrint(testString)
        if error:
            indentedPrint(message)
            indentedPrint("ERROR: Target is {}".format(target))
        else:
            indentedPrint("OK")

        indentedPrint()
    
    
    #test 2 : bare terrain + feature
    t.addFeature("FT_TEST")
    testString = "FOOD:{}, PROD:{}, COMM:{}, MOVE:{}, DEF:{}".format(t.foodYield,t.productionYield,t.commerceYield,t.travelCost, t.defensiveBonus)
    target = "FOOD:4, PROD:3, COMM:7, MOVE:0.5, DEF:100"
    error = target != testString
    if error :
        message = "ERROR: feature computation failed"
        out_messages.append(message)
    if verbose:
        indentedPrint(t)
        indentedPrint(testString)
        if error:
            indentedPrint(message)
            indentedPrint("ERROR: Target is {}".format(target))
        else:
            indentedPrint("OK")
        indentedPrint()
    
    
    indentedPrint("testTileComputation END: {} errors".format(len(out_messages)))
    if verbose: print()
    
    return out_messages

def testCSVLoad(verbose, filename, header):
    #init
    if verbose:
        indentedPrint("testCSVLoad START->{}".format(filename))
    out_messages = []
    
    #check the headers
    with open(filename, newline ="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        firstRow = ";".join(next(reader))
        target = header
        error = target != firstRow
        if error :
            message = "ERROR: {} header is wrong".format(filename)
            out_messages.append(message)
        if verbose:
            indentedPrint("{} header test".format(filename))
            indentedPrint("READED:"+firstRow)
            if error:
                indentedPrint(message)
                indentedPrint("ERROR: TARGET IS:{}".format(target))
            else:
                indentedPrint("OK")
            indentedPrint()

    
    indentedPrint("testCSVLoad END->{}: {} errors".format(filename,len(out_messages)))
    if verbose: print()
    
    return out_messages

def runTests(verbose = False):
    messages = []
    print("##### MAPTESTS START")
    messages += testTileComputation(verbose)
    messages += testCSVLoad(verbose,"terrains.csv","key;name;description;foodYield;productionYield;commerceYield;travelCost;defensiveBonus;availableFeatures;terrainType")
    messages += testCSVLoad(verbose,"features.csv","key;terrain;name;description;requires;constraints;type;workAmount;specials")
    messages += testCSVLoad(verbose,"buildings.csv","key;name;description;hammerCost;purchaseCost;maintenance;requires;obsoletedBy")
    messages += testCSVLoad(verbose,"buildings_specials.csv","buildingKey;specialKey;arg1;arg2;comment")
    
    print("##### MAPTESTS END: {} errors".format(len(messages)))
    for m in messages:
        indentedPrint(m)
    if not verbose:
        print("Activate verbose for more info")
    return messages

runTests()
