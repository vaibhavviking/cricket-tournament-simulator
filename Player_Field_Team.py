import numpy as np

class Team:

    def __init__(self,name,batsmen,bowlers,fanRatio,fieldSize,pitchType):
        self.name = name
        self.batsmen = batsmen
        self.bowlers = bowlers
        self.field = Field(fanRatio,fieldSize,pitchType)



class Player:

    def __init__(self,name,battingExp,bowlingExp,wideProb,noBallProb,lbwProb):
        self.name = name
        self.battingExp = battingExp
        self.bowlingExp = bowlingExp
        self.wideProb = wideProb
        self.noBallProb = noBallProb
        self.lbwProb = lbwProb

    def getBall(self):
        factor = np.random.uniform()
        if factor < self.wideProb:
            return 'wide'
        elif factor < self.wideProb+self.noBallProb:
            return 'noball'
        elif factor < self.wideProb+self.noBallProb+self.lbwProb:
            return 'lbw'
        else: 
            return 'fair'
        
    def getRuns(self):
        factor = np.random.uniform()
        if factor < self.battingExp/4:
            return 6
        elif factor < self.battingExp/2:
            return 4
        else:
            return np.random.randint(4)

    def isOut(self):
        factor = np.random.uniform(0,0.8)
        if factor > self.battingExp:
            return 1
        else:
            return 0

class Field:

    def __init__(self,fanRatio,fieldSize,pitchType):
        self.fanRatio = fanRatio
        self.fieldSize = fieldSize
        self.pitchType = pitchType