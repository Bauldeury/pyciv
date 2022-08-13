updateId = 0

def getSpecialExists(items,searchedItem):
    '''-items: must be a dict of items
    ---item: must have a list of specials called "specials", string list\n
    -searchedItem'''
    if items == None:
        return False
    else:
        for i in items:
            if items[i].specials != None :
                if searchedItem in items[i].specials:
                    output = True
    return False
    
def getSpecialValueSum(items,searchedItem):
    '''-items: must be a dict of items
    ---item: must have a list of specials called "specials", string list'''
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
    '''-items: must be a dict of items
    ---item: must have a list of specials called "specials", string list'''
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
    '''-items: must be a dict of items
    ---item: must have a list of specials called "specials", string list'''
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
    '''-items: must be a dict of items
    ---item: must have a list of specials called "specials", string list'''
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

def decomposeStrToArgs(string:str,boolArgs:"list[str]"=[],intArgs:"list[str]"=[],strArgs:"list[str]"=[]) -> "dict[str,bool|str]":
    '''INPUT:
    All args must be only one letter.
    If the arg doesn't exist it's not shown.
    If the arg exist multiple times only the last one will appear.
    Separator is !
    - string: string to analyse
    - boolArg: check whether the arg is present in the string or not
    - intArg: check all digits|- just after the arg
    - strArg: check all char just after the arg, stops when Separator is found
    \nOUTPUT:
    - a dictionary of the values found for the args, output[arg] = value'''
    
    i = 0
    imax = len(string)
    output = dict()
    separator = '!'

    while i < imax:
        if string[i] in boolArgs:
            output[string[i]] = True
            i+= 1

        elif string[i] in intArgs:
            arg = string[i]
            i+=1
            x = ""
            while i < imax and (string[i].isdigit() or string[i] == '-'):
                x+=string[i]
                i+=1
            #if string[i] in output: output[string[i]] += separator
            output[arg] = x

        elif string[i] in strArgs:
            arg = string[i]
            i+=1
            x = ""
            while i < imax and string[i] != separator:
                x+=string[i]
                i+=1
            #if string[i] in output: output[string[i]] += separator
            output[arg] = x
        else:
            i+=1

    return output

    
# print (__name__)