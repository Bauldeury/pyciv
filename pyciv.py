import map
import city
import building
import unit

turn = 0

def _init():
    pass

def endTurn():
    global turn
    turn += 1
    print("\nYEAR {}".format(turn-8000))
    
    city.helper.endTurn()


_init()