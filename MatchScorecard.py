import numpy as np

class MatchScorecard:
    """
    Match Scorecard stores overall runs scored by batsmen and bowling figures for both the teams

    ...

    Attributes
    ----------

    batsmen : list of dictionaries
        [player_name : {player,runs,balls}] for each team
    bowlers : list of dictionaries
        [player_name : {player,runs,balls,wickets,wides,noballs}] for each team
    innings : 0 if first innings 1 if second innings
    runsScored : [runs scored by first batting team, runs scored by second batting team] 
                    for NRR calculation
    ballsFaced : [balls faced by second batting team, balls faced by first batting team]
    batFirst : Team
        The team which is batting first
    bowlFirst : Team
        The team which if bowling first

    Methods
    --------
    batsmanDismissal(str,Player,Player,Player)
    getBowler(bowler)
    getRandomFielder()
    bowlerUpdate(changes)
    batsmanUpdate(changes)

    """

    def __init__(self,teamA,teamB,batFirst):
        self.batsmen = [] #(batsman,runs,balls)
        self.bowlers = [] #(bowler,runs,balls,wickets,wides,noballs)

        temp = {}
        for batsmen in teamA.batsmen:   # populate batsmen from teamA
            temp[batsmen.name] = [batsmen,0,0]
        self.batsmen.append(temp)
        temp = {}   
        for batsmen in teamB.batsmen:   # populate batsmen from teamB
            temp[batsmen.name] = [batsmen,0,0]
        
        temp = {}
        for bowler in teamA.batsmen:    # populate bowlers from teamA
            temp[bowler.name] = [bowler,0,0,0,0,0]
        self.bowlers.append(temp)
        self.batsmen.append(temp)
        temp = {}
        for bowler in teamB.batsmen:    # populate bowlers from teamB
            temp[bowler.name] = [bowler,0,0,0,0,0]
        self.bowlers.append(temp)

        self.innings = 0
        self.runsScored = [0,0]
        self.ballsFaced = [0,0]
        self.batFirst = batFirst
        self.bowlFirst = teamA
        if teamA==batFirst:
            self.bowlFirst = teamB

    def batsmanDismissal(self,method,batsman,bowler,fielder):
        """
        updates the scorecard when a batsman is out.
        """
        
        # add details about the dismissal to the batsman dictionary entry
        if method=='bowled':    
            self.batsmen[self.innings][batsman.name].extend(['bowled',bowler])
        elif method=='runout':
            self.batsmen[self.innings][batsman.name].extend(['runout',bowler,fielder])
        elif method=='caught':
            self.batsmen[self.innings][batsman.name].extend(['runout',bowler,fielder])
        elif method=='lbw':
            self.batsmen[self.innings][batsman.name].extend(['lbw',bowler])
    
    def getBowler(self,bowler):
        """
        chooses a bowler from the bowling team other than the one bowling now.
        """
        # continue searching for bowlers while a different bowler is not found
        while True:
            ind = np.random.randint(len(self.bowlers[self.innings]))
            if list(self.bowlers[self.innings])[ind][0] != bowler:
                return list(self.bowlers[self.innings].values())[ind][0]
    
    def getRandomFielder(self):
        """
        chooses a random player from the bowling team as fielder in case of runout,catch out.
        """

        ind = np.random.randint(len(self.batsmen[1-self.innings]))
        return list(self.batsmen[1-self.innings].values())[ind][0]

    def bowlerUpdate(self,changes):
        """
        updates bowler stats for the current match after each ball.
        """

        for j in range(1,6):
            self.bowlers[self.innings][changes[0].name][j]+=changes[j]

    def batsmanUpdate(self,changes):
        """
        updates batsman stats for the current match after each ball.
        """
        for j in range(1,3):
            self.batsmen[self.innings][changes[0].name][j]+=changes[j]
