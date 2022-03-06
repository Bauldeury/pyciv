print(" ____  __    __  ____  ___ __      __")
print("|  _ \ \ \  / / / ___//_ _/\ \    / /")
print("| |_) | \ \/ / | |     | |  \ \  / / ")
print("|  __/   |  |  | |___  | |   \ \/ /  ")
print("|_|      |__|   \____//___/   \__/   ")
print()
                                
import map
import city
import building
import unit
import player

#vars

turn = 0
currentYear = -8000
mp = None

def _init():
    player.helper.registerEndTurnListener(endTurn)

    global mp
    mp = map.map(50,25)
    
    p0 = player.player()
    p0.name = "Barbarians"
    p0.leaderName = "Barbarator"
    p0.adjective = "barbarian"
    p0.color = "C31A1A"
    p0.color2 = "393939"
    p0.canDoDiplomacy = False
    
    p1 = player.player()
    p1.name = "Francia"
    p1.leaderName = "Player"
    p1.adjective = "frank"
    p1.color = "2E63CD"
    p1.color2 = "393939"
    
    p2 = player.player()
    p2.name = "Holy Roman Empire"
    p2.leaderName = "Barberousse"
    p2.adjective = "holy roman"
    p2.color = "EED221"
    p2.color2 = "393939"
    
    c1 = city.city(name = "Paris", owner = p1.key, tile = mp.getTile(1,1))
    
    
    c2 = city.city(name = "Berlin", owner = p2.key, tile = mp.getTile(5,5))
    
def advanceYear():
    global currentYear

    if currentYear < -2000:
        currentYear += 100
        
    elif currentYear < 0:
        currentYear += 50
        
    elif currentYear < 1000:
        currentYear += 25
        
    elif currentYear < 1500:
        currentYear += 10
        
    elif currentYear < 1750:
        currentYear += 5
        
    elif currentYear < 1850:
        currentYear += 2
        
    else:
        currentYear += 1

def endTurn():
    global turn
    
    city.helper.endTurn()
    player.helper.endTurn()
    
    turn += 1
    advanceYear()
    
    print("TURN {}: YEAR {}".format(turn,currentYear))
    player.helper.startTurn()


_init()

player.helper.getPlayer(0).endTurn()
player.helper.getPlayer(1).endTurn()
player.helper.getPlayer(2).endTurn()