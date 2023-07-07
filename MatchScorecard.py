import numpy as np

class MatchScorecard:

    def __init__(self,teamA,teamB,batFirst):
        self.batsmen = [] #(batsman,runs,balls)
        self.bowlers = [] #(bowler,runs,balls,wickets,wides,noballs)
        temp = []
        for batsmen in teamA.batsmen:
            temp.append([batsmen,0,0])
        self.batsmen.append(temp)
        temp = []
        for bowler in teamA.batsmen:
            temp.append([bowler,0,0,0,0,0])
        self.bowlers.append(temp)
        temp = []
        for batsmen in teamB.batsmen:
            temp.append([batsmen,0,0])
        self.batsmen.append(temp)
        temp = []
        for bowler in teamB.batsmen:
            temp.append([bowler,0,0,0,0,0])
        self.bowlers.append(temp)
        self.innings = 0
        self.runsScored = [0,0]
        self.ballsFaced = [0,0]
        self.batFirst = batFirst
        self.bowlFirst = teamA
        if teamA==batFirst:
            self.bowlFirst = teamB

    def batsmanDismissal(self,method,batsman,bowler,fielder):
        for i in range(len(self.batsmen)):
            if self.batsmen[self.innings][i][0].name == batsman.name:
                if method=='bowled':
                    self.batsmen[self.innings][i].extend(['bowled',bowler])
                elif method=='runout':
                    self.batsmen[self.innings][i].extend(['runout',bowler,fielder])
                elif method=='caught':
                    self.batsmen[self.innings][i].extend(['runout',bowler,fielder])
                elif method=='lbw':
                    self.batsmen[self.innings][i].extend(['lbw',bowler])
    
    def getBowler(self,bowler):
        while True:
            ind = np.random.randint(len(self.bowlers[self.innings]))
            print(self.bowlers[self.innings][ind][0])
            if self.bowlers[self.innings][ind][0] != bowler:
                return self.bowlers[self.innings][ind][0]
    
    def getRandomFielder(self):
        ind = np.random.randint(len(self.batsmen[1-self.innings]))
        return self.batsmen[1-self.innings][ind][0]

    def bowlerUpdate(self,changes):
        for i in range(len(self.bowlers[self.innings])):
            if changes[0].name == self.bowlers[self.innings][i][0].name:
                for j in range(1,5):
                    self.bowlers[self.innings][i][j]+=changes[j]

    def batsmanUpdate(self,changes):
        for i in range(len(self.batsmen[self.innings])):
            if changes[0].name == self.batsmen[self.innings][i][0].name:
                for j in range(1,2):
                    self.batsmen[self.innings][i][j]+=changes[j]
