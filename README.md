# FPL-Guru
A Tkinter app using FPL (Fantasy Premier League) API and linear programming along with convex numerical optimization to analyze real-time data and optimally produce a playing 11 for weekly PL matches
##### For more information, refer to the [Documentation](https://github.com/hoodarm/FPL-Guru/tree/main/Documentation) directory or watch a [video](https://youtu.be/OiX2t5Wn2ks) explanation

## What is FPL?
FPL is an online fantasy football game where participants, acting as virtual team managers, create teams using players from the Premier League. Players have different price tags based on their perceived skill and performance. With a budget constraint, participants must manage wisely to build competitive teams. Points are earned based on real-life player performances, including goals, assists, and clean sheets, while negative actions lead to deductions. Managers can change their team lineup weekly for added flexibility.

### FPL rules and constraints for team selection
1.  <ins>Budget constraint</ins>: The total value of the squad must not exceed £100 million.
2.  <ins>Club constraint</ins>: A maximum of 3 players can be chosen from a single Premier League club.
3.  <ins>Positional constraint</ins>: The squad must be made of 15 players, consisting of 2 goalkeepers (GK), 5 defenders (DF), 5 midfielders (MF), and 3 forwards (FW)

## Basics of FPL Guru
1. Analyses footballer performances based on statistics such as goals scored, assists made, tackles, xG (expected goals), etc
2. Assigns each player a score on an index determined by pre-defined criteria.
3. Upon comparing different player performances, cost, budget, and restrictions, an optimum team for the upcoming game week is suggested.
4. Also allows for comparison between different players head-to-head for preferential selection
5. Considers individual player performances in recent weeks and percentage player selection by FPLers before producing the optimal team.

## Major algorithmic problems tackled (refer to Documentation for detailed info)
1) Working with FPL API and extracting official data
2) Data management and storage of extracted statistics
3) Defining a form rating index
4) Ranking players on a relative form rating index
5) Determining the optimum team per week based on financial, positional, and club constraints
6) Creating a dynamic GUI based on buttons/choices clicked
7) Displaying optimum team (working with background image and grid placing)
8) Modifying a table view based on user’s selection of options
