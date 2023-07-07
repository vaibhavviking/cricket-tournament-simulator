import numpy as np
from Match import Match
from utils import generateTeam

class Tournament:
    
    def __init__(self,teams):
        self.teams = teams
        self.matchesPlayed = 0
        self.status = {}
        for team in teams:
            self.status[team.name]={}
            self.status[team.name]['matches_played'] = 0
            self.status[team.name]['team'] = team
            self.status[team.name]['nrr'] = 0
            self.status[team.name]['points'] = 0
    
    def playLeagueMatches(self):
        for teamAind in range(len(self.teams)):
            for teamBind in range(len(self.teams)):
                    if teamAind == teamBind:
                        continue
                    teamA = self.teams[teamAind]
                    teamB = self.teams[teamBind]

                    self.playMatch(teamA,teamB)

    def playMatch(self,teamA,teamB):
        self.matchesPlayed += 1
        self.status[teamA.name]['matches_played'] += 1
        self.status[teamB.name]['matches_played'] += 1

        myMatch = Match(teamA,teamB,teamA,2,0.6)
        
        loserTeam = teamB
        result=[0]
        
        while result==[0]:
            result = myMatch.playBall()
            print(result)
            if result[0]==teamA:
                print(teamA.name + ' has won the game')
            elif result[0]==teamB:
                print(teamB.name + ' has won the game')
        
        runs = myMatch.umpire.matchScorecard.runsScored
        balls = myMatch.umpire.matchScorecard.ballsFaced
        
        if teamA != result[0]:
            loserTeam = teamA
        
        nrrs = [runs[0]/balls[1],runs[1],balls[0]]

        if result[1]==1:
            prevNrr = self.status[result[0].name]['nrr']
            self.status[result[0].name]['nrr'] = (prevNrr + nrrs[1])/2
            
            prevNrr = self.status[loserTeam.name]['nrr']
            self.status[loserTeam.name]['nrr'] = (prevNrr + nrrs[0])/2

        else:
            prevNrr = self.status[result[0].name]['nrr']
            self.status[result[0].name]['nrr'] = (prevNrr + nrrs[0])/2
            
            prevNrr = self.status[loserTeam.name]['nrr']
            self.status[loserTeam.name]['nrr'] = (prevNrr + nrrs[1])/2

        self.status[result[0].name]['points'] += 1
        return loserTeam

    def playFinal(self,teamA,teamB):
        loserTeam = self.playMatch(teamA,teamB)
        winnerTeam = teamA
        if loserTeam == teamA:
            winnerTeam = teamB
        print(winnerTeam.name+' has won the tournament')


import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def main():
    teams = []
    for i in range(6):
        teams.append(generateTeam('Team-'+str(i+1)))
    mytourney = Tournament(teams)
    blockPrint()
    mytourney.playLeagueMatches()
    enablePrint()
    stats = sorted(list(mytourney.status.values()), key= lambda i : (-i['points'],-i['nrr']))
    print(list(stats))
    mytourney.playFinal(stats[0]['team'],stats[1]['team'])

main()