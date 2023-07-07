import numpy as np
from MatchScorecard import MatchScorecard

class Umpire:

    def __init__(self,teamA,teamB,prob,batFirst):
        self.runs = 0
        self.wickets = 0
        self.balls = 0
        self.bowler = teamB.bowlers[0]
        self.batsman = teamA.batsmen[0]
        self.nonStriker = teamA.batsmen[1]
        self.matchScorecard = MatchScorecard(teamA,teamB,batFirst)
        self.lbwProb = prob
        self.runs=0
        self.balls=0

    def wideUpdator(self):
        self.runs += 1
        self.matchScorecard.bowlerUpdate([self.bowler,1,0,0,1,0])

    def noBallUpdator(self):
        self.runs += 1
        self.matchScorecard.bowlerUpdate([self.bowler,1,0,0,0,1])
    
    def runUpdator(self,runs,battingTeam=None):
        if battingTeam is not None:
            self.matchScorecard.runsScored[self.matchScorecard.innings] += runs
            self.matchScorecard.ballsFaced[1-self.matchScorecard.innings] += 1
        self.runs += runs
        self.balls += 1
        self.matchScorecard.bowlerUpdate([self.bowler,runs,1,0,0,0])
        self.matchScorecard.batsmanUpdate([self.batsman,runs,1])
        if runs%2 == 1:
            self.changeStrike()

    def dismissalUpdator(self,method):
        self.wickets += 1
        bowlerWicket = 0
        if method != 'runout':
            bowlerWicket = 1
        self.matchScorecard.bowlerUpdate([self.bowler,0,1,bowlerWicket,0,0])
        fielder = None
        if method == 'runout' or method == 'caught':
            fielder = self.matchScorecard.getRandomFielder()
        self.matchScorecard.batsmanDismissal(method,self.batsman,self.bowler,fielder)
        if self.wickets != 10: 
            self.batsman = self.matchScorecard.batsmen[self.matchScorecard.innings][self.wickets+1][0]

    def overUpdator(self):
        self.changeStrike()
        self.bowler = self.matchScorecard.getBowler(self.bowler)
        
    def changeStrike(self):
        temp = self.batsman
        self.batsman = self.nonStriker
        self.nonStriker = temp

    def changeInnings(self):
        self.runs = self.balls = self.wickets = 0
        self.matchScorecard.innings=1
        self.bowlers = self.matchScorecard.bowlers[1][0][0]
        self.batsman = self.matchScorecard.batsmen[1][0][0]
        self.nonStriker = self.matchScorecard.batsmen[1][0][0]

    def decideLbw(self):
        factor = np.random.uniform()
        if factor <= 0.3:
            return 1
        else:
            return 0