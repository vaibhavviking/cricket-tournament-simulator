import numpy as np
from Player_Field_Team import Player,Team

def generateRandomPlayer(batsman,name):
    """
    generates a random player with random stats.
    """
    # initially player has bowling stats higher
    batlow = 0
    bathigh = 0.5
    ballow = 0.5
    balhigh = 1
    if batsman: # increase batting stats if we are generating a batsman
        batlow = 0.5
        bathigh =1
        ballow = 0
        balhigh = 0.5

    # Generate player
    player = Player(name,np.random.uniform(batlow,bathigh),
                    np.random.uniform(ballow,balhigh),
                    np.random.uniform(0,0.1),
                    np.random.uniform(0,0.1),
                    np.random.uniform(0,0.1)
                    )
    return player

def generateTeam(name):
    """
    generates a 11 player team with 5 bowlers with random stats.
    """

    teamBatsmen = []
    for i in range(11):
        batsman = True
        if i>5: # the last 5 batsman are bowlers
            batsman = False
        teamBatsmen.append(generateRandomPlayer(batsman,'Player-'+str(i+1)))

    teamBowlers = teamBatsmen[-5:] # the last 5 players are bowlers

    # randomaly generated data
    fanRatio = np.random.uniform(0.4,0.6)
    pitchType = np.random.randint(2)
    fieldSize = np.random.uniform(60,70)

    # Generate team
    team = Team(name,teamBatsmen,teamBowlers,fanRatio,fieldSize,pitchType)
    return team

def getRandomDismissal():
    """
    selects a random way of dismissal
    """
    
    ways = ['bowled','runout','caught']
    return ways[np.random.randint(3)]