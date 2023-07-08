import numpy as np
from Umpire import Umpire
from Commentator import Commentator
from utils import getRandomDismissal

class Match:
    """
    Class Match represents one single match between two teams

    ...

    Attributes
    -----------
    teams : list
        list of the two teams where the 0-index team bats first
    overs : int
        total number of overs in an innings
    target : int
        target set by the first team for the second team
    umpire : Umpire
        Umpire object to keep track of the match status
    commentator : Commentator
        Commentator object for commentary

    ...

    Methods
    -------
    playBall(Team,Team,Team,int,float):
        advances the play of the game by one ball
    postBallHandler(bool):
        updates the state of the appropriate objects after each ball and
        checks for the end of innings/match
    """

    def __init__(self,teamA,teamB,homeOf,overs,umpireProb):
        self.teams = []
        self.commentator = Commentator()
        self.overs = overs
        self.target = None

        randNum = np.random.uniform(1) # toss
        batFirst = teamA
        if randNum>0.5: 
            self.commentator.announce(f'{teamA.name} has won the toss')
            if homeOf == teamA or homeOf.field.fieldSize<65:  # if ground is small or is home ground winning team chooses to bat first
                self.commentator.announce(f'{teamA.name} has elected to bat first')
                self.teams = [teamA,teamB]
            else:
                self.commentator.announce(f'{teamA.name} has elected to bowl first')
                self.teams = [teamB,teamA]
                batFirst = teamB                
        else:
            self.commentator.announce(f'{teamB.name} has won the toss')
            if homeOf==teamB or homeOf.field.fieldSize<65: 
                self.commentator.announce(f'{teamB.name} has elected to bat first')
                self.teams = [teamB,teamA]
                batFirst = teamB
            else:
                self.commentator.announce(f'{teamB.name} has elected to bowl first')
                self.teams = [teamA,teamB]
        
        self.umpire = Umpire(self.teams[0],self.teams[1],umpireProb,batFirst)
        
        

    def playBall(self):
        """
        Advances the game by one ball and makes necessary updates in the states.

        Returns:
        list: [winning_team,winning_team_batting_number] incase match has ended else [0]

        """
        self.commentator.announce(f'Overs: {int(self.umpire.balls//6) +1}.{self.umpire.balls%6}')
        ball = self.umpire.bowler.getBall() # the type of ball bowled by the bowler
        fair=True # nature of ball (fair/extra)
        if ball == 'wide': # wide
            fair=False
            self.commentator.announce(f'{self.umpire.bowler.name} bowled a wide')
            self.umpire.wideUpdator()
        elif ball == 'noball': # no-ball
            fair=False
            self.commentator.announce(f'{self.umpire.bowler.name} bowled a no ball')
            self.umpire.noBallUpdator()
            pass
        elif ball == 'lbw': # lbw
            self.commentator.announce(f'{self.umpire.bowler.name} bowled a lbw')
            decision = self.umpire.decideLbw()
            if decision == 0: # out
                self.commentator.announce(f'{self.umpire.batsman.name} is out')
                self.umpire.dismissalUpdator('lbw')     # handle lbw dismissal
                self.commentator.announce(f'{self.umpire.batsman.name} has come to the crease')
            else:   # not out
                self.commentator.announce(f'{self.umpire.batsman.name} is not out')
                self.umpire.runUpdator(0)   # update team runs
            pass
        else:
            self.commentator.announce(f'{self.umpire.bowler.name} bowled a fair delivery')
            isout = self.umpire.batsman.isOut()     # whether batsman has got out on the ball
            if isout == 0: # batsman is not out
                runs = self.umpire.batsman.getRuns()
                self.commentator.announce(f'{self.umpire.batsman.name} has scored ' + str(runs) + ' runs')
                self.umpire.runUpdator(runs,self.teams[self.umpire.matchScorecard.innings]) # update runs
            else:   # batsman is out
                dismissal = getRandomDismissal()    # get a random dismissal (except lbw)
                self.commentator.announce(f'{self.umpire.batsman.name} has got {dismissal}')
                self.umpire.dismissalUpdator(dismissal)
                if self.umpire.wickets < 10:    # only announce if match has not ended
                    self.commentator.announce(f'{self.umpire.batsman.name} has come to the crease')
        
        self.commentator.ballUpdate(self.umpire)    # ball-by-ball update by the commentator
        return self.postBallHandler(fair)   # update states and check for end of innings/match

    def postBallHandler(self,fair):
        """
        Called at the end of every ball to check whether game has ended or should continue
        -also makes updates incase over is up

        Return:
        list: [winning_team,winning_team_batting_number] incase match has ended else [0]

        """

        # target chased
        if self.target != None and self.target <= self.umpire.runs:
            self.commentator.announce(f'Target has been chased successfully by {self.teams[1].name}')
            self.commentator.announce(f'{self.teams[1].name} wins the game by {10-self.umpire.wickets} wickets!')
            return [self.teams[1],1] # [winning team, innings in which they batted]
        
        # team is all out
        if self.umpire.wickets == 10:
            self.commentator.announce('team is allout!')
            if self.umpire.matchScorecard.innings == 0:     # first innings has concluded
                self.commentator.announce('Innings is over...')
                self.target = self.umpire.runs
                self.commentator.announce(f'{self.teams[1].name} must chase {self.target} runs to win this game')
                self.umpire.changeInnings()
            else:   # chasing team has got all out
                self.commentator.announce('Target was not chased successfully')
                self.commentator.announce(f'{self.teams[0].name} wins the game by {self.target - self.umpire.runs} runs!')
                return [self.teams[0],0] # [winning team, innings in which they batted]
        
        # over up
        if fair==True and self.umpire.balls % 6 == 0:
            if self.umpire.balls == self.overs*6:   # check whether the innings is complete
                if self.umpire.matchScorecard.innings == 0: # first innings has concluded
                    self.commentator.announce('Innings is complete')
                    self.target = self.umpire.runs  # update the target
                    self.commentator.announce(f'{self.teams[1].name} must chase {self.target} runs to win this game')
                    self.umpire.changeInnings() # change the innings
                else:   # chasing team has run out of balls
                    self.commentator.announce('Target was not chased successfully')
                    self.commentator.announce(f'{self.teams[0].name} wins the game by {self.target - self.umpire.runs} runs!')
                    return [self.teams[0],0] # [winning team, innings in which they batted]
                pass
            else:   # innings is not complete and the game continues
                self.commentator.announce('Over is up!')
                self.commentator.overSummary(self.umpire.overString)
                if self.target is not None: # if second innings then print runs required
                    self.commentator.announce(f'{self.teams[1].name} needs {self.target - self.umpire.runs} runs within {self.overs*6 - self.umpire.balls} balls to win this game')
                self.umpire.overUpdator()   # update over specific states
                self.commentator.announce(f'{self.umpire.bowler.name} is bowling this over')
        return [0] # signifies that game is not complete yet