import csv  
import requests, json
from pprint import pprint
from IPython.display import display
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# base url for all FPL API endpoints
base_url = 'https://fantasy.premierleague.com/api/'

# get data from bootstrap-static endpoint
r = requests.get(base_url+'bootstrap-static/').json()

# create players dataframe
players = pd.json_normalize(r['elements'])

# show some information about first five players
players[['id', 'web_name', 'team', 'element_type']].head()

# create teams dataframe
teams = pd.json_normalize(r['teams'])

# get position information from 'element_types' field
positions = pd.json_normalize(r['element_types'])

positions.head()

# join players to teams
df = pd.merge(left=players, right=teams, left_on='team', right_on='id')

# join player positions
df = df.merge(positions, left_on='element_type', right_on='id')

# rename columns
df = df.rename(columns={'name':'team_name', 'singular_name':'position_name'})

with open('Data_analysis/PlayerBasicData.csv', 'w') as f:
    writer = csv.writer(f)
    for i in range(0, 726):
        content_list=[]
        content_list.append(df.iloc[i]["first_name"] + " " + df.iloc[i]["second_name"])
        content_list.append(df.iloc[i]["position_name"])
        content_list.append(df.iloc[i]["team_name"])
        writer.writerow(content_list)

text = open("Data_analysis/PlayerBasicData.csv", "r")
text = ''.join([i for i in text]).replace("Forward", "FW")
text = ''.join([i for i in text]).replace("Midfielder", "MF")
text = ''.join([i for i in text]).replace("Defender", "DF")
text = ''.join([i for i in text]).replace("Goalkeeper", "GK")
text = ''.join([i for i in text]).replace("Man City", "Manchester City")
text = ''.join([i for i in text]).replace("Man Utd", "Manchester United")
text = ''.join([i for i in text]).replace("Nott'm Forest", "Nottingham Forest")
text = ''.join([i for i in text]).replace("Spurs", "Tottenham Hotspur")
x = open("Data_analysis/PlayerBasicData.csv","w")
x.writelines(text)
x.close()


with open('Data_analysis/PlayerSeasonData.csv', 'w') as f:
    writer = csv.writer(f)
    for i in range(0, 726):
        content_list=[]
        content_list.append(df.iloc[i]["first_name"] + " " + df.iloc[i]["second_name"])
        content_list.append(df.iloc[i]["minutes"])
        content_list.append(df.iloc[i]["goals_scored"])
        content_list.append(df.iloc[i]["assists"])
        content_list.append(df.iloc[i]["clean_sheets"])
        content_list.append(df.iloc[i]["goals_conceded"])
        content_list.append(df.iloc[i]["own_goals"])
        content_list.append(df.iloc[i]["penalties_saved"])
        content_list.append(df.iloc[i]["penalties_missed"])
        content_list.append(df.iloc[i]["yellow_cards"])
        content_list.append(df.iloc[i]["red_cards"])
        content_list.append(df.iloc[i]["saves"])
        content_list.append(df.iloc[i]["starts"])
        content_list.append(df.iloc[i]["expected_goals"])
        content_list.append(df.iloc[i]["expected_assists"])
        content_list.append(df.iloc[i]["expected_goal_involvements"])
        content_list.append(df.iloc[i]["expected_goals_conceded"])
        writer.writerow(content_list)

# create dataframe for different keys of dictionary 'r'
player_stats = pd.json_normalize(r['elements'])
positions_info = pd.json_normalize(r['element_types'])
teams = pd.json_normalize(r['teams'])
list_of_stats = pd.json_normalize(r['element_stats'])
deadlines_gameweek = pd.json_normalize(r['events'])
gameweeks_per_month = pd.json_normalize(r['phases'])
# total_players = pd.json_normalize(r['total_players'])
gamesettings = pd.json_normalize(r['game_settings'])
file1 = open('Data_analysis/myfile.txt', 'w')
file1.write(player_stats.to_string())

for i in range(0,38):
    print(deadlines_gameweek.iloc[i]["name"] + ": " + deadlines_gameweek.iloc[i]["deadline_time"])

#minutes, goals_scored, assists, clean_sheets, goals_conceded, own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards, saves, starts, expected_goals, expected_assists, expected_goal_involvements, expected_goals_conceded
#"Minutes", "Goals", "Assists", "Penalties missed", "Yellow cards", "Red cards", "Starts", "xG", "xA"
#Minutes, Clean sheets, Goals conceded, Penalties saved, Yellow cards, Red cards, Saves, Starts, Expected goals conceded
#Minutes, Goals, Assists, Clean sheets, Goals conceded, Yellow cards, Red cards, Starts, Expected goal involvements