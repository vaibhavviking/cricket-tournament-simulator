import numpy as np
from utils import generateTeam
from Tournament import Tournament
import sys
import os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def main():
    numTeams = 0
    while numTeams < 2:
        numTeams = int(input("Enter the number of teams (atleast 2): "))
    overs = 0
    while overs < 1:
        overs = int(input("Enter the number of overs per match (minimum 1): "))
    teams = []
    for i in range(numTeams):
        teamName = input(f'Enter the name for team no. {i+1} : ')
        teams.append(generateTeam(teamName))

    myTourney = Tournament(teams,overs) # create an instance of a Tournament

    userPrompt = int(input('Enter 1 if you wish to prompted after every ball otherwise 0: '))

    myTourney.playLeagueMatches(userPrompt) 


    stats = sorted(list(myTourney.status.values()), 
                    key= lambda i : (-i['points'],-i['nrr']))  # chose the top two teams for final
    
    myTourney.playFinal(stats[0]['team'],stats[1]['team'],userPrompt)

main()
