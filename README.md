# Cricket Tournament Simulator

CTS is a simple console program that can simulate a cricket tournament containing user-inputted number of teams. 

- League Matches are played first
- Final is played by the top two teams in the points table

## Features

- Randomly generates players with varying batting and bowling expertise
- Randomly generates teams consisting of these random players
- User can give names to these teams
- Ball by Ball score updates the commentator functionality
- Fully automatic with minimal user input required

## How to run

- Clone this repository in a folder of your choice
- run the command 'python main.py' to execute the top level script (replace 'python' with the alias of your python version)
- Enter the required data into the console
- Wait for the simulation to be over and a winning team to be decided


## Details about the simulator

The whole simulator can be broken down into the following classes:
- Tournament : Manages matches between the teams and maintains the points table
- Match : Simulates a single match between two teams 
- Umpire : Keeps track of all necessary data about an ongoing match
- MatchScorecard : Keeps track of the batting and bowling figures of a match
- Team : Consists of players among whom some are bowlers
- Player : Possesses batting and bowling EXP which decides the runs scored and wickets taken
- Field : Home ground of a team affects a team's decision after winning toss
- Commentary : Ball-by-Ball updates are given using this class
