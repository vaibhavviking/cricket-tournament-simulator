from Match import Match
from Commentator import Commentator
import time
class Tournament:
    """
    Tournament stores data about a particular tournament

    ...

    Attributes
    ----------
    teams : list of Teams
        all the teams playing in the tournament
    matchesPlayed : int
        total matches played till now
    status : dict
        current standings of teams in the tournament
    commentator : Commentator
    
    Methods
    -------

    playLeagueMatches():
        conducts all the required league matches
    playMatch(Team,Team):
        conducts a single match
    playFinal(Team,Team):
        conducts the finale of the tournament
    """
    
    def __init__(self,teams,overs):
        self.teams = teams
        self.matchesPlayed = 0
        self.status = {}
        self.commentator = Commentator()
        self.overs = overs

        # all the teams have 0 stats initially
        for team in teams:
            self.status[team.name]={}
            self.status[team.name]['matches_played'] = 0
            self.status[team.name]['team'] = team
            self.status[team.name]['nrr'] = 0
            self.status[team.name]['points'] = 0
    
    def playLeagueMatches(self,userPrompt):
        """
        simulates all the league matches of the tournament
        For N teams there are N*(N-1) league matches.
        """
        # conduct 2 matches between each pair of teams
        for teamAind in range(len(self.teams)):
            for teamBind in range(len(self.teams)):
                    if teamAind == teamBind:
                        continue
                    teamA = self.teams[teamAind]
                    teamB = self.teams[teamBind]
                    self.commentator.announce(f'Match no. {self.matchesPlayed+1} is between {teamA.name} and {teamB.name}')

                    loserTeam = self.playMatch(teamA,teamB,userPrompt)
                    
                    self.commentator.announce('Onto the next match!')
        print('')
        print('--------FINAL MATCH OF THE TOURNAMENT-------')


    def playMatch(self,teamA,teamB,userPrompt):
        """
        simulates the play of a single match.

        Return:
        loserTeam (Team) : the losing team

        """

        # increment the tournament states
        self.matchesPlayed += 1
        self.status[teamA.name]['matches_played'] += 1
        self.status[teamB.name]['matches_played'] += 1

        myMatch = Match(teamA,teamB,teamA,self.overs,0.6) # conduct match
        
        loserTeam = teamB
        result=[0]
        
        while result==[0]:  # while result is not returned keep playing balls
            result = myMatch.playBall()
            if userPrompt == 1:
                input()
            
        
        runs = myMatch.umpire.matchScorecard.runsScored # runs scored by each team
        balls = myMatch.umpire.matchScorecard.ballsFaced # balls faced by each team
        
        if teamA != result[0]:  
            loserTeam = teamA
        
        nrrs = [runs[0]/balls[1],runs[1],balls[0]]  # calculate the nrr of this particular match for both teams

        # calculate new nrr by taking average (just for representation of nrr)
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

        self.status[result[0].name]['points'] += 1  # increment points of the winning team
        return loserTeam

    def playFinal(self,teamA,teamB,userPrompt):
        """
        simulates the play of the final match.

        args:
        teamA (Team) : Team which is on top after league matches
        teamB (Team) : Team which is on 2nd after league matches
        """
        self.commentator.announce(f'The final match is between {teamA.name} and {teamB.name}')
        loserTeam = self.playMatch(teamA,teamB,userPrompt) 
        winnerTeam = teamA
        if loserTeam == teamA:
            winnerTeam = teamB
        print(str(winnerTeam.name)+' has won the tournament')
