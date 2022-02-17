import city
import building

turn = 0
cities = []

def __init():
    capital = city.city(name="Capital")
    cities.append(capital)
    capital.buildings.add("PALACE")
    capital.buildings.add("PALACE")
    capital.buildings.add("GRANARY")

def endturn():
    global turn
    turn += 1
    print("\nYEAR {}".format(turn-8000))
    
    global cities
    for c in cities:
        c.endTurn()


__init()