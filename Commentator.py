class Commentator:
    
    def announce(self,announcement):
        """
        prints miscellaneous commentaries.
        """

        print(announcement)
        print('')
    
    def overSummary(self,overString):
        """
        prints a summary of the over.
        """
        
        runs=0
        wickets=0
        for ball in overString:
            if ball == 'w':
                wickets+=1
            elif ball == 'wd':
                runs += 1
            elif ball == 'nb':
                runs += 1
            else:
                runs += int(ball)
        
        print(str(runs)
                + ' runs scored in this over and '
                + str(wickets) + ' wickets fell')
        print('')

    def ballUpdate(self,umpire):
        """
        Prints ball-by-ball updates 
        """
        runs = umpire.runs
        wickets = umpire.wickets
        batsmanName = umpire.batsman.name
        batsmanRuns = umpire.matchScorecard.batsmen[umpire.matchScorecard.innings][batsmanName][1]
        batsmanBalls = umpire.matchScorecard.batsmen[umpire.matchScorecard.innings][batsmanName][2]
        nonStrikerName = umpire.nonStriker.name
        nonStrikerRuns = umpire.matchScorecard.batsmen[umpire.matchScorecard.innings][nonStrikerName][1]
        nonStrikerBalls = umpire.matchScorecard.batsmen[umpire.matchScorecard.innings][nonStrikerName][2]
        print(f'Score: {runs}-{wickets}',end=' | ')
        print(f'{batsmanName}* - {batsmanRuns}({batsmanBalls})',end=' | ')
        print(f'{nonStrikerName} - {nonStrikerRuns}({nonStrikerBalls})')
        print('')