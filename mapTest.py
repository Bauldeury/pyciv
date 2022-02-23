import map

def printInstance(ins):
    print('\n'.join("{}:{}".format(k,v) for k,v in ins.__dict__.items()))

mymap = map.map(10,10)

print()
print("TERRAIN TEST: DESERT")
t = map._terrains["DESERT"]
printInstance(t)
del t

print()
print("FEATURE TEST: RAILROAD")
# f = 1
# printInstance(f)
# del f