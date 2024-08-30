# FPL-Guru
A Tkinter app using FPL (Fantasy Premier League) API to analyze player data and optimally produce a playing 11 for weekly PL matches

## What is FPL?
FPL is an online fantasy football game where participants, acting as virtual team managers, create teams using players from the Premier League. Players have different price tags based on their perceived skill and performance. With a budget constraint, participants must manage wisely to build competitive teams. Points are earned based on real-life player performances, including goals, assists, and clean sheets, while negative actions lead to deductions. Managers can change their team lineup weekly for added flexibility. (https://www.premierleague.com/news/2173986)

### FPL rules and constraints for team selection
A.  Budget constraint: The total value of the squad must not exceed £100 million.
B.  Club constraint: A maximum of 3 players can be chosen from a single Premier League club.
C.  Positional constraint: The squad must be made of 15 players, consisting of 2 goalkeepers (GK), 5 defenders (DF), 5 midfielders (MF), and 3 forwards (FW)

## Basics of FPL Guru
1. Analyses footballer performances based on statistics such as goals scored, assists made, tackles, xG (expected goals), etc
2. Assigns each player a score on an index determined by pre-defined criteria.
3. Upon comparing different player performances, cost, budget, and restrictions, an optimum team for the upcoming game week is suggested.
4. Also allows for comparison between different players head-to-head for preferential selection
5. Considers individual player performances in recent weeks and percentage player selection by FPLers before producing the optimal team.

## Major algorithmic problems tackled
