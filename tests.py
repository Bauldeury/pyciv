import mymap
import city
import building
import unit

import csv

def printInstance(ins):
    print('\n'.join("{}:{}".format(k,v) for k,v in ins.__dict__.items()))
    
def indentedPrint(txt = ""):
    print("|_ {}".format(txt))

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
    
def testTileComputation(verbose):
    #init
    if verbose:
        indentedPrint("testTileComputation START")
        indentedPrint()
    out_messages = []

    #basic data
    tr = mymap._terrain("TR_TEST")
    tr.foodYield = 3
    tr.productionYield = 2
    tr.commerceYield = 1
    tr.travelCost = 1
    tr.defensiveBonus = 0
    mymap._terrains[tr.key] = tr
    if verbose:
        indentedPrint(tr)
        indentedPrint("FOOD:{}, PROD:{}, COMM:{}, MOVE:{}, DEF:{}".format(tr.foodYield,tr.productionYield,tr.commerceYield,tr.travelCost, tr.defensiveBonus) )
        indentedPrint()
    
    ft = mymap._feature(("FT_TEST","TR_TEST"))
    ft.specials = ["COMMERCE_YIELD","4","DEFENSIVE_BONUS","100","SET_MOVEMENT_COST","0.5","ALL_MULTIPLIER","1.5"]
    mymap._features[ft.key] = ft
    if verbose:
        indentedPrint(ft)
        indentedPrint(ft.specials)
        indentedPrint()
    
    t = mymap.tile()
    t.terrain = mymap._terrains["TR_TEST"]
    
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

def testBuildings(verbose):
    #init
    if verbose:
        indentedPrint("testBuildings START")
        indentedPrint()
    out_messages = []
    
    #basic data
    blds = building.buildingSet()
    #test buildings
    building1 = building._building("BUILDING1")
    building2 = building._building("BUILDING2")
    s1 = 3
    s2 = 5
    building1.specials = ["POP_SUPPORT",s1]
    building2.specials = ["POP_SUPPORT",s2]
    
    #test 1: no building
    target = 0
    erreur = (blds.special("POP_SUPPORT") != target)
    if erreur:
        message = "ERROR: POP_SUPPORT target is {}. Calculated value is {}".format(target,blds.special("POP_SUPPORT"))
        out_messages.append(message)
    if verbose:
        indentedPrint(blds)
        indentedPrint(blds.specials)
        if erreur: indentedPrint(message)
    
    #test 2: adding the building1
    try:
        blds.add("BUILDING1")
    except BaseException as err:
        out_messages.append("{}:{}".format(type(err),err))
        return out_messages
    
    target = s1
    erreur = (blds.special("POP_SUPPORT") != target)
    if erreur:
        message = "ERROR: POP_SUPPORT target is {}. Calculated value is {}".format(target,blds.special("POP_SUPPORT"))
        out_messages.append(message)
    if verbose:
        indentedPrint(blds)
        indentedPrint(blds.specials)
        if erreur: indentedPrint(message)
    
    #test 3: adding the building2
    try:
        blds.add("BUILDING2")
    except BaseException as err:
        out_messages.append("{}:{}".format(type(err),err))
        return out_messages
    
    target = s1+s2
    erreur = (blds.special("POP_SUPPORT") != target)
    if erreur:
        message = "ERROR: POP_SUPPORT target is {}. Calculated value is {}".format(target,blds.special("POP_SUPPORT"))
        out_messages.append(message)
    if verbose:
        indentedPrint(blds)
        indentedPrint(blds.specials)
        if erreur: indentedPrint(message)
    
    #test 4:removing the building1
    try:
        blds.remove("BUILDING1")
    except BaseException as err:
        out_messages.append("{}:{}".format(type(err),err))
        return out_messages
    
    target = s2
    erreur = (blds.special("POP_SUPPORT") != target)
    if erreur:
        message = "ERROR: POP_SUPPORT target is {}. Calculated value is {}".format(target,blds.special("POP_SUPPORT"))
        out_messages.append(message)
    if verbose:
        indentedPrint(blds)
        indentedPrint(blds.specials)
        if erreur: indentedPrint(message)
    
    
    
    indentedPrint("testBuildings END: {} errors".format(len(out_messages)))
    if verbose: print()
    
    return out_messages

def runTests(verbose = False):
    messages = []
    print("##### TESTS START")
    messages += testTileComputation(verbose)
    messages += testCSVLoad(verbose,"terrains.csv","key;name;description;foodYield;productionYield;commerceYield;travelCost;defensiveBonus;availableFeatures;terrainType")
    messages += testCSVLoad(verbose,"features.csv","key;terrain;name;description;requires;constraints;type;workAmount;specials")
    messages += testCSVLoad(verbose,"buildings.csv","key;name;description;hammerCost;maintenance;requires;obsoletedBy;specials")
    messages += testBuildings(verbose)
    
    print("##### TESTS END: {} errors".format(len(messages)))
    for m in messages:
        indentedPrint(m)
    if not verbose:
        print("Activate verbose for more info")
    return messages

runTests()
