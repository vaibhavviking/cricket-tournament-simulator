import numpy as np
from MatchScorecard import MatchScorecard

class Umpire:
    """
    Umpire keeps the current data about the match

    ...

    Attributes
    ----------

    runs : int
        current innings score

    wickets : int
        current innings wicket

    balls : int
        current innings ball bowled

    bowler : Player
        current bowler

    batsman : Player
        current batsman batting

    nonStriker : Player
        batsman on the other end

    matchScorecard : MatchScorecard
        stores overall match data

    lbwProb : float between 0 and 1
        probability that umpire adjudges lbw out

    overString : list
        each ball data of current over

    Methods
    -------
    
    wideUpdator()
    noBallUpdator()
    runUpdator()
    dismissalUpdator()
    overUpdator()
    changeStrike()
    changeInnings()
    decideLbw()

    """

    def __init__(self,teamA,teamB,prob,batFirst):
        self.runs = 0
        self.wickets = 0
        self.balls = 0
        self.bowler = teamB.bowlers[0]
        self.batsman = teamA.batsmen[0]
        self.nonStriker = teamA.batsmen[1]
        self.matchScorecard = MatchScorecard(teamA,teamB,batFirst)
        self.lbwProb = prob
        self.overString=[]

    def wideUpdator(self):
        """
        updates states in case of wide.
        """

        self.runs += 1  # batting team gets 1 run
        self.overString.append('wd')    # update over string
        self.matchScorecard.bowlerUpdate([self.bowler,1,0,0,1,0])

    def noBallUpdator(self):
        """
        updates states in case of a no ball.
        """

        self.runs += 1  # batting team gets 1 runs
        self.overString.append('nb')    # update over string
        self.matchScorecard.bowlerUpdate([self.bowler,1,0,0,0,1])
    
    def runUpdator(self,runs,battingTeam=None):
        """
        updates states in case runs are scored.
        """

        if battingTeam is not None: # if runs are not by extra then update nrr data
            self.matchScorecard.runsScored[self.matchScorecard.innings] += runs
            self.matchScorecard.ballsFaced[1-self.matchScorecard.innings] += 1

        self.overString.append(str(runs))
        self.runs += runs
        self.balls += 1
        self.matchScorecard.bowlerUpdate([self.bowler,runs,1,0,0,0])
        self.matchScorecard.batsmanUpdate([self.batsman,runs,1])

        if runs%2 == 1:     # if batsman scored 1 or 3 runs then change strike
            self.changeStrike()

    def dismissalUpdator(self,method):
        """
        updates states in case of a batsman gets out.
        """

        self.wickets += 1
        self.overString.append('w')
        self.balls += 1

        bowlerWicket = 0   
        if method != 'runout':  # dont update bowler wicket if runout
            bowlerWicket = 1

        self.matchScorecard.bowlerUpdate([self.bowler,0,1,bowlerWicket,0,0])

        fielder = None
        if method == 'runout' or method == 'caught':    # generating fielder responsible for catch/runout
            fielder = self.matchScorecard.getRandomFielder()

        self.matchScorecard.batsmanDismissal(method,self.batsman,self.bowler,fielder)

        if self.wickets != 10: # send new batsman if team if not all out
            self.batsman = list(self.matchScorecard.batsmen[self.matchScorecard.innings].values())[self.wickets+1][0]

    def overUpdator(self):
        """
        updates states at the end of the over.
        """

        self.changeStrike()
        self.overString = []
        self.bowler = self.matchScorecard.getBowler(self.bowler)
        
    def changeStrike(self):
        """
        swaps batsman and non-striker when running between wickets.
        """

        temp = self.batsman
        self.batsman = self.nonStriker
        self.nonStriker = temp

    def changeInnings(self):
        """
        changes the states when the first innings end.
        """

        self.overString = []
        self.runs = self.balls = self.wickets = 0
        self.matchScorecard.innings=1
        self.bowlers = list(self.matchScorecard.bowlers[1].values())[0][0]
        self.batsman = list(self.matchScorecard.batsmen[1].values())[0][0]
        self.nonStriker = list(self.matchScorecard.batsmen[1].values())[1][0]

    def decideLbw(self):
        factor = np.random.uniform()
        if factor <= 0.3:   # umpire adjudges lbw out
            return 1
        else:
            return 0