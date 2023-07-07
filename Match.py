import numpy as np
from Player_Field_Team import Field
from Umpire import Umpire

class Match:

    def __init__(self,teamA,teamB,homeOf,overs,umpireProb):
        self.teams = []
        randNum = np.random.uniform(1)
        batFirst = teamA
        if randNum>0.5:
            print('Team A has won the toss')
            if homeOf.field.fieldSize<65:
                print('Team A has elected to bat first')
                self.teams = [teamA,teamB]
            else:
                print('Team A has elected to bowl first')
                self.teams = [teamB,teamA]
                batFirst = teamB                
        else:
            if homeOf.field.fieldSize<65:
                print('Team B has elected to bat first')
                self.teams = [teamB,teamA]
                batFirst = teamB
            else:
                print('Team B has elected to bowl first')
                self.teams = [teamA,teamB]
        self.overs = overs
        self.umpire = Umpire(self.teams[0],self.teams[1],umpireProb,batFirst)
        self.target = None

    def playBall(self):
        print('Bowling ball no. '+str(self.umpire.balls+1))
        ball = self.umpire.bowler.getBall()
        fair=True
        if ball == 'wide': # wide
            fair=False
            print('bowler bowled a wide')
            self.umpire.wideUpdator()
        elif ball == 'noball': # no-ball
            fair=False
            print('bowler bowled a no ball')
            self.umpire.noBallUpdator()
            pass
        elif ball == 'lbw': # lbw
            print('bowler bowled a lbw')
            decision = self.umpire.decideLbw()
            if decision == 0: # out
                print('batsman is out')
                self.umpire.dismissalUpdator('lbw')
            else:   # not out
                print('batsman is not out')
                self.umpire.runUpdator(0)
            pass
        else:
            print('bowler bowled a fair delivery')
            isout = self.umpire.batsman.isOut()
            if isout == 0:
                runs = self.umpire.batsman.getRuns()
                print('batsman has scored ' + str(runs) + ' runs')
                self.umpire.runUpdator(runs,self.teams[self.umpire.matchScorecard.innings])
            else:
                print('batsman has got caught')
                self.umpire.dismissalUpdator('caught')
        
        print('The score is ' + str(self.umpire.runs) + ' - ' + str(self.umpire.wickets))
        return self.postBallHandler(fair)

    def postBallHandler(self,fair):
        # target chased
        if self.target != None and self.target <= self.umpire.runs:
            print('Target has been chased successfully')
            return [self.teams[1],1]
        
        # team is all out
        if self.umpire.wickets == 10:
            print('team is allout')
            if self.umpire.matchScorecard.innings == 0:
                print('Innings is over')
                self.target = self.umpire.runs
                self.umpire.changeInnings()
            else:
                print('target was not chased successfully')
                return [self.teams[0],0]
        
        # over up
        if fair==True and self.umpire.balls % 6 == 0:
            print('Over is up')
            if self.umpire.balls == self.overs*6:
                if self.umpire.matchScorecard.innings == 0:
                    print('Innings is complete')
                    self.target = self.umpire.runs
                    self.umpire.changeInnings()
                else:
                    print('Target was not chased successfully')
                    return [self.teams[0],0]
                pass
            else:
                self.umpire.overUpdator()
        return [0]