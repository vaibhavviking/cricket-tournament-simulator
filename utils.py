import numpy as np
from Player_Field_Team import Player,Team

def generateRandomPlayer(batsman,name):
    batlow = 0
    bathigh = 0.5
    ballow = 0.5
    balhigh = 1
    if batsman:
        batlow = 0.5
        bathigh =1
        ballow = 0
        balhigh = 0.5

    player = Player(name,np.random.uniform(batlow,bathigh),
                    np.random.uniform(ballow,balhigh),
                    np.random.uniform(0,0.1),
                    np.random.uniform(0,0.1),
                    np.random.uniform(0,0.1)
                    )
    return player

def generateTeam(name):
    teamBatsmen = []
    for i in range(11):
        batsman = True
        if i>5:
            batsman = False
        teamBatsmen.append(generateRandomPlayer(batsman,'Player-'+str(i+1)))
    teamBowlers = teamBatsmen[-5:]
    fanRatio = np.random.uniform(0.4,0.6)
    pitchType = np.random.randint(2)
    fieldSize = np.random.uniform(60,70)
    team = Team(name,teamBatsmen,teamBowlers,fanRatio,fieldSize,pitchType)
    return team
