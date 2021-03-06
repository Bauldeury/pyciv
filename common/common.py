def getSpecialExists(items,searchedItem):
#-items: must be a dict of items
#---item: must have a list of specials called "specials", string list
#-searchedItem
    if items == None:
        return False
    else:
        for i in items:
            if items[i].specials != None :
                if searchedItem in items[i].specials:
                    output = True
    return False
    
def getSpecialValueSum(items,searchedItem):
#-items: must be a dict of items
#---item: must have a list of specials called "specials", string list
    if items == None:
        return 0.0
    else:
        output = 0.0
        for i_it in items:
            sps = items[i_it].specials
            if sps != None:
                for i_sp in range(len(sps)-1):
                    if searchedItem == sps[i_sp]:
                        output += float(sps[i_sp+1])
        return output

def getSpecialValueProduct(items,searchedItem):
#-items: must be a dict of items
#---item: must have a list of specials called "specials", string list
    if items == None:
        return 1.0
    else:
        output = 1.0
        for i_it in items:
            sps = items[i_it].specials
            if sps != None:
                for i_sp in range(len(sps)-1):
                    if searchedItem == sps[i_sp]:
                        output *= float(sps[i_sp+1])
        return output
        
def getSpecialValueMax(items,searchedItem):
#-items: must be a dict of items
#---item: must have a list of specials called "specials", string list
    if items == None:
        return None
    else:
        output = None
        for i_it in items:
            sps = items[i_it].specials
            if sps != None:
                for i_sp in range(len(sps)-1):
                    if searchedItem == sps[i_sp]:
                        inspectedValue = float(sps[i_sp+1])
                        if (output == None or output < inspectedValue):
                            output = inspectedValue
        return output
    
def getSpecialValueMin(items,searchedItem):
#-items: must be a dict of items
#---item: must have a list of specials called "specials", string list
    if items == None:
        return None
    else:
        output = None
        for i_it in items:
            sps = items[i_it].specials
            if sps != None:
                for i_sp in range(len(sps)-1):
                    if searchedItem == sps[i_sp]:
                        inspectedValue = float(sps[i_sp+1])
                        if (output == None or output > inspectedValue):
                            output = inspectedValue
        return output
        
def getCommonPath():
    if __package__ == None:
        return ""
    elif __package__ == "common":
        return "common/"
    
# print (__name__)