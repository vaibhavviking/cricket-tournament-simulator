import numpy as np

class Team:
    """
    Team stores data about all the batsmen and bowlers in a team and their home ground
    (Note that all the bowlers are assumed to also be batsmen and hence also exist in the 
        batsmen attribute)

    ...

    Attribute
    ---------
    name : str
        name of the team
    batsmen : list of Players
        consists of all players
    bowlers : list of Player
        consists of only bowlers
    field : Field
        home ground of the team

    Methods
    -------
    battingOrder(list)
        changes batting order according to input
        returns : updated batting order
    listOfPlayers()
        returns: list of all players in the team
    """

    def __init__(self,name,batsmen,bowlers,fanRatio,fieldSize,pitchType):
        self.name = name
        self.batsmen = batsmen
        self.bowlers = bowlers
        self.field = Field(fanRatio,fieldSize,pitchType)
    
    def battingOrder(self,lineUp):
        """
        changes the batting order.

        arguments:
        lineUp (list) : a permutation of indices which denotes the new batting order

        """

        self.batsmen = [self.batsmen[index] for index in lineUp]
    
    def listOfPlayers(self):
        """
        return the list of all players in a team.
        """

        players = []
        for batsman in self.batsmen:
            players.append(batsman.__dict__)
        return players

class Player:
    """
    Player stores the data about a particular player

    Attributes
    ----------
    name : str
        name of the player
    battingExp : float between 0 and 1
        batting experience of the player
    bowlingExp : float between 0 and 1
        bowling experience of the player
    wideProb : float between 0 and 0.1
        probability of throwing a wide ball
    noBallProb : float between 0 and 0.1
        probability of throwing a no ball
    lbwProb : float between 0 and 0.1
        probability of getting the batsman LBW
    
    Methods
    -------
    getBall():
        returns the type of ball thrown by a player (fair,wide,noball)
    getRuns():
        returns the runs scored by the player on a delivery
    isOut():
        return the probability of the batsman being out

    """

    def __init__(self,name,battingExp,bowlingExp,wideProb,noBallProb,lbwProb):
        self.name = name
        self.battingExp = battingExp
        self.bowlingExp = bowlingExp
        self.wideProb = wideProb
        self.noBallProb = noBallProb
        self.lbwProb = lbwProb

    def getBall(self):
        """
        decides the nature of the ball (fair,wide,etc.) on the basis of bowler stats.
        """

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
        """
        returns the runs scored by batsman on fair delivery on the basis of the batsman stats.
        """

        factor = np.random.uniform()
        if factor < self.battingExp/4:
            return 6
        elif factor < self.battingExp/2:
            return 4
        else:
            return np.random.randint(4)

    def isOut(self):
        """
        decides if the batsman is out on the basis of the batsman stats.
        """
        factor = np.random.uniform(0,0.8)
        if factor > self.battingExp:
            return 1
        else:
            return 0

class Field:
    """
    Field stores the data about a particular ground

    ...

    Attributes: 
    -----------

    fanRatio : float between 0 and 1
        ratio of number of fans of both the teams
    fieldSize : int
        size of the field
    pitchType : 0 or 1
        type of pitch (0 if bowling 1 if batting)
    """
    
    def __init__(self,fanRatio,fieldSize,pitchType):
        self.fanRatio = fanRatio
        self.fieldSize = fieldSize
        self.pitchType = pitchType