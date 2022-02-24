import map

def printInstance(ins):
    print('\n'.join("{}:{}".format(k,v) for k,v in ins.__dict__.items()))

mymap = map.map(10,10)

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

print()
print("YIELD TEST: PLAINS, WHEAT, IRRIGATION,RAILROAD")
t = map.tile()
t.addFeature("WHEAT")
t.addFeature("IRRIGATION")
t.addFeature("RAILROAD")
print("FOOD:{}".format(t.foodYield))
print("TRAVEL_COST:{}".format(t.travelCost))
del t

