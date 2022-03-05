_players = {}
class player:
    def __init__(self):
        self.key = 0
        self.name = "CivName"
        self.leaderName = "LeaderName"
        self.adjective = "civnamian"
        self.color = "FF0000"
        self.color2 = "FFFF00"
        
        self.techs = set()
        self.gold = 100
    
    def __repr__(self):
        return "C_PLAYER#{}".format(self.key)
        