from tkinter import simpledialog
from tkinter import Canvas
import cvxpy as cp
import numpy as np
import random
import csv  
import customtkinter as ct
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv  
import requests
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

teams.head()

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
        content_list.append(df.iloc[i]["total_points"])
        content_list.append(df.iloc[i]["now_cost"])
        content_list.append(df.iloc[i]["cost_change_start"])
        content_list.append(df.iloc[i]["selected_by_percent"])
        content_list.append(df.iloc[i]["web_name"])
        writer.writerow(content_list)

#minutes, goals_scored, assists, clean_sheets, goals_conceded, own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards, saves, starts, expected_goals, expected_assists, expected_goal_involvements, expected_goals_conceded
#"Minutes", "Goals", "Assists", "Penalties missed", "Yellow cards", "Red cards", "Starts", "xG", "xA"

clubWisePlayerData={}
positionWisePlayerData = {}
players_data = []
players_statistics = []
playernames = []
clubs = []
positions = ["DF", "FW", "MF", "GK"]
gameweekDeadlines = {}

# read player data from CSV file
with open ('Data_analysis/PlayerBasicData.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        individualPlayer = {}
        individualPlayer['name'] = line[0]
        playernames.append(line[0])
        individualPlayer['position'] = line[1]
        individualPlayer['club'] = line[2]
        if (line[2] not in clubs):
            clubs.append(line[2])
        players_data.append(individualPlayer)

for club in clubs:
    playersintheclub = []
    for player in playernames:
        for playerID in players_data:
            if (playerID["club"] == club and playerID["name"] == player):
                playersintheclub.append(playerID["name"])
    clubWisePlayerData[club] = playersintheclub

for position in positions:
    playersintheposition = []
    for player in playernames:
        for playerID in players_data:
            if (playerID["position"] == position and playerID["name"] == player):
                playersintheposition.append(playerID["name"])
    positionWisePlayerData[position] = playersintheposition

#read player season statistics
with open ('Data_analysis/PlayerSeasonData.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        individualPlayer = {}
        individualPlayer["Name"] = line[0]
        individualPlayer["Minutes"] = line [1]
        individualPlayer["Goals"] = line [2]
        individualPlayer["Assists"] = line [3]
        individualPlayer["Clean sheets"] = line [4]
        individualPlayer["Goals conceded"] = line [5]
        individualPlayer["Own goals"] = line [6]
        individualPlayer["Penalties saved"] = line [7]
        individualPlayer["Penalties missed"] = line [8]
        individualPlayer["Yellow cards"] = line [9]
        individualPlayer["Red cards"] = line [10]
        individualPlayer["Saves"] = line [11]
        individualPlayer["Starts"] = line [12]
        individualPlayer["xG"] = line [13]
        individualPlayer["xA"] = line [14]
        individualPlayer["Expected goal involvements"] = line [15]
        individualPlayer["Expected goals conceded"] = line [16]
        individualPlayer["Total points"] = line [17]
        individualPlayer["Current cost"] = int(line [18])
        individualPlayer["Change of cost to the start"] = line [19]
        individualPlayer["Form rating"] = 0
        individualPlayer["Position"] = ""
        individualPlayer["Relative form rating"] = 0
        individualPlayer["Club"] = ""
        individualPlayer["Percentage selection"] = float(line [20])/100
        individualPlayer["Web name"] = line [21]
        players_statistics.append(individualPlayer)

# FW    
# 0.4 - Goals
# 0.3 - Assists
# 0.2 - xG
# 0.1 - Minutes

# MF
# 0.4 - Assists
# 0.3 - Goals
# 0.2 -xA
# 0.1 - Minutes

# GK
# 0.6 - Saves
# 0.5 - Clean sheets
# -0.2 - Goals conceded
# 0.1 - Penalties saved

# DF
# 0.4 - Clean sheets
# 0.3 - Starts
# 0.2 - Goals
# 0.1 - Assists

for item in players_statistics:
        if item["Name"] in positionWisePlayerData["GK"]:
            item["Form rating"] = round(0.1 * float(item["Saves"]) + 0.8 * float(item["Clean sheets"]) - 0.2 * float(item["Goals conceded"]) + 0.1 * float(item["Penalties saved"]) + 0.1 * float(item["Total points"]) + 0.2 * float(item["Percentage selection"]),1)
            item ["Position"] = "GK"

for item in players_statistics:
        if item["Name"] in positionWisePlayerData["DF"]:
            item["Form rating"] = round(0.4 * float(item["Clean sheets"]) + 0.1 * float(item["Starts"]) + 0.2 * float(item["Goals"]) + 0.1 * float(item["Assists"]) + 0.1 * float(item["Total points"]) + 0.2 * float(item["Percentage selection"]),1)
            item ["Position"] = "DF"
            
for item in players_statistics:
        if item["Name"] in positionWisePlayerData["FW"]:
            item["Form rating"] = round(0.5 * float(item["Goals"]) + 0.1 * float(item["Assists"]) + 0.05 * float(item["xG"]) + 0.1 * float(item["Total points"]) + 0.2 * float(item["Percentage selection"]),1)
            item ["Position"] = "FW"

for item in players_statistics:
        if item["Name"] in positionWisePlayerData["MF"]:
            item["Form rating"] = round(0.25 * float(item["Assists"]) + 0.4 * float(item["Goals"]) + 0.05 * float(item["xA"]) + 0.1 * float(item["Total points"]) + 0.2 * float(item["Percentage selection"]),1)
            item ["Position"] = "MF"

for club, players in clubWisePlayerData.items():
    for player in players:
        for player2 in players_statistics:
            if (player2["Name"] == player):
                player2["Club"] = club

def get_line_from_file(file_path, line_number):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if 1 <= line_number <= len(lines):
                return lines[line_number - 1]  # Adjust line_number to 0-based index
            else:
                return "Line number out of range."
    except FileNotFoundError:
        return "File not found."

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=1500, height=800)

        self.controller = controller
        self.menu_bar = None

        #setting background image
        background_image = Image.open("GUI/bg_image.jpg")
        background_image = background_image.resize((1500, 800), Image.ANTIALIAS)
        background_image = ImageTk.PhotoImage(background_image)        

        background_label = tk.Label(self, image=background_image)
        background_label.image = background_image  # Keep a reference to the image
        background_label.place(relwidth=1, relheight=1)  # Make the label cover the entire frame

        # create welcome frame
        self.welcome_frame = ct.CTkFrame(self, corner_radius=0)
        self.welcome_frame.grid(row=0, column=0, sticky="")  # Remove sticky attribute for the welcome_frame

        self.welcome_frame.place(x=575, y=230)
        self.welcome_label = ct.CTkLabel(self.welcome_frame, text="FPL Guru",
                                                font=ct.CTkFont(size=50, weight="bold", family='Helvetica'))
        self.welcome_label.grid(row=0, column=0, padx=60, pady=(50, 5))
        self.welcome_button = ct.CTkButton(self.welcome_frame, text="Continue", command=self.welcome, width=200)
        self.welcome_button.grid(row=3, column=0, padx=30, pady=(15, 45))

    def welcome(self):
        print("welcome successful")
        messagebox.showinfo("Success", "Welcome to FPL Guru!")
        self.create_menu_bar()
        self.controller.config(menu=self.menu_bar)
        self.controller.show_frame(MyTeamPage_Pitch)

    def create_menu_bar(self):
        # Create the menu bar
        self.menu_bar = tk.Menu(self.controller)

        # Create menus for each frame
        myteam_menu = tk.Menu(self.menu_bar, tearoff=0)
        playercomp_menu = tk.Menu(self.menu_bar, tearoff=0)
        player_menu = tk.Menu(self.menu_bar, tearoff=0)
        tips_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="Best Team", menu=myteam_menu)
        self.menu_bar.add_cascade(label="Player Comparison", menu=playercomp_menu)
        self.menu_bar.add_cascade(label="Players", menu=player_menu)
        self.menu_bar.add_cascade(label="Tips", menu=tips_menu)

        myteam_menu.add_command(label="Best Team", command=lambda: self.controller.show_frame(MyTeamPage_Pitch))
        playercomp_menu.add_command(label="Head-to-Head", command=lambda: self.controller.show_frame(PlayerCompPage_Head))
        playercomp_menu.add_command(label="Form rating", command=lambda: self.controller.show_frame(PlayerCompPage_Form))
        player_menu.add_command(label="Player list", command=lambda: self.controller.show_frame(PlayersPage))
        tips_menu.add_command(label="Tips", command=lambda: messagebox.showinfo("Tips", get_line_from_file("Data_analysis/tips.txt", random.randint(1, 70))))


class MyTeamPage_Pitch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "white")

        # Create a Auto-Suggest button for suggesting the possible transfers/inital team
        self.auto_suggest = ct.CTkButton(self, text = "Auto-Suggest", 
                                         width=120, height=32, border_width=0 ,corner_radius=15, 
                                         fg_color='green', hover = True, hover_color='grey', command= self.auto_suggest_team)
        self.auto_suggest.place(relx=0.95, rely=0.08, anchor = "ne")
        # Create a canvas for the pitch
        self.pitch_canvas = Canvas(self, width=900, height=540, bg='white', highlightthickness=0, highlightbackground='white')
        self.pitch_canvas.pack()
        self.pitch_canvas.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.background_image = Image.open("GUI/Canvas.jpg")
        self.background_image = self.background_image.resize((900, 540), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Display the background image on the canvas
        self.pitch_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Create a dropdown menu for choosing formation
        optionmenu_var = ct.StringVar(value="Choose formation")  # set initial value
        self.choose_formation = ct.CTkOptionMenu(self, values = ["4-4-2", "4-5-1", "3-5-2",
                                                "5-4-1"], variable=optionmenu_var, width=170, height = 30) 
        self.choose_formation.place(relx=0.95, rely= 0.15, anchor ="ne")

        maxPlayerRating = 0

        for player in players_statistics:
            if player["Position"] == "FW":
                current_player_form_rating = player["Form rating"]
                if current_player_form_rating>maxPlayerRating:
                    maxPlayerRating = current_player_form_rating

        for player in players_statistics:
            if player["Position"] == "FW":
                player ["Relative form rating"] = round(player["Form rating"]/(maxPlayerRating)*100,1)

        maxPlayerRating = 0

        for player in players_statistics:
            if player["Position"] == "GK":
                current_player_form_rating = player["Form rating"]
                if current_player_form_rating>maxPlayerRating:
                    maxPlayerRating = current_player_form_rating

        for player in players_statistics:
            if player["Position"] == "GK":
                player ["Relative form rating"] = round(player["Form rating"]/(maxPlayerRating)*100,1)

        maxPlayerRating = 0

        for player in players_statistics:
            if player["Position"] == "DF":
                current_player_form_rating = player["Form rating"]
                if current_player_form_rating>maxPlayerRating:
                    maxPlayerRating = current_player_form_rating

        for player in players_statistics:
            if player["Position"] == "DF":
                player ["Relative form rating"] = round(player["Form rating"]/(maxPlayerRating)*100,1)

        maxPlayerRating = 0

        for player in players_statistics:
            if player["Position"] == "MF":
                current_player_form_rating = player["Form rating"]
                if current_player_form_rating>maxPlayerRating:
                    maxPlayerRating = current_player_form_rating

        for player in players_statistics:
            if player["Position"] == "MF":
                player ["Relative form rating"] = round(player["Form rating"]/(maxPlayerRating)*100,1)
    
    def auto_suggest_team (self):
        # Get the selected formation from the dropdown
        selected_formation = self.choose_formation.get()

        # Prompt the user for positional weights
        position_weights = self.get_position_weights()

        formation_counts = {'GK': 1, 'DF': 0, 'MF': 0, 'FW': 0}

        # Define formation counts for each formation
        formation_counts_mapping = {
            '4-4-2': {'DF': 4, 'MF': 4, 'FW': 2},
            '3-5-2': {'DF': 3, 'MF': 5, 'FW': 2},
            '4-5-1': {'DF': 4, 'MF': 5, 'FW': 1},
            '5-4-1': {'DF': 5, 'MF': 4, 'FW': 1},
        }

        formation_counts.update(formation_counts_mapping[selected_formation])
        player_data = players_statistics

        # Extract relevant information from player data
        relative_form = np.array([player["Relative form rating"] for player in player_data])
        cost = np.array([player["Current cost"] for player in player_data])
        positions = np.array([player["Position"] for player in player_data])
        clubs = np.array([player["Club"] for player in player_data])

        # Apply position weights to relative form ratings
        weighted_relative_form = np.array([position_weights[pos] * rating for pos, rating in zip(positions, relative_form)])

        # Define the optimization variables
        x = cp.Variable(len(player_data), boolean=True)

        # Define the optimization problem
        objective = cp.Maximize(cp.sum(x * weighted_relative_form))
        constraints = [
            cp.sum(x * cost) <= 1000,
            cp.sum(x * cost) >= 990,
            cp.sum(x[positions == "GK"]) == 2,
            cp.sum(x[positions == "DF"]) == 5,
            cp.sum(x[positions == "MF"]) == 5,
            cp.sum(x[positions == "FW"]) == 3,
        ]

        # Additional constraint: No more than three players from a single club
        for club in set(clubs):
            constraints.append(cp.sum(x[clubs == club]) <= 3)

        problem = cp.Problem(objective, constraints)

        # Solve the problem
        problem.solve()

        # Display the results
        selected_players = [player_data[i] for i in range(len(player_data)) if x.value[i] == 1]

        sorted_players = sorted(selected_players, key=lambda x: x["Relative form rating"], reverse=True)
        selected_team = {'GK': [], 'DF': [], 'MF': [], 'FW': []}

        for pos, count in formation_counts.items():
            for player in sorted_players:
                if (player["Position"] == pos) and len(selected_team[pos])<count:
                    selected_team[pos].append(player)

        self.display_team_on_pitch(selected_team)

    def get_position_weights(self):
        # Prompt the user for positional weights
        weights_str = simpledialog.askstring("Positional Weights", "Enter positional weights separated by commas (e.g., 1,2,4,3) in the order GK, DF, MF, FW:")

        # Convert the string input to a list of integers
        try:
            weights = list(map(int, weights_str.split(',')))
        except ValueError:
            # Handle invalid input (non-integer values)
            tk.messagebox.showerror("Error", "Invalid input. Please enter integer values separated by commas.")
            return {"GK": 1, "DF": 2, "MF": 4, "FW": 3}

        # Validate that the number of weights matches the number of positions
        if len(weights) == 4:
            return {"GK": weights[0], "DF": weights[1], "MF": weights[2], "FW": weights[3]}
        else:
            # Handle invalid input (wrong number of weights)
            tk.messagebox.showerror("Error", "Invalid input. Please enter exactly 4 positional weights.")
            return {"GK": 1, "DF": 2, "MF": 4, "FW": 3}
    
    def display_team_on_pitch(self, team):
        # Clear previous drawings
        self.pitch_canvas.delete("all")
        self.background_image = Image.open("GUI/Canvas.jpg")
        self.background_image = self.background_image.resize((900, 540), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Display the background image on the canvas
        self.pitch_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Draw players on the pitch based on their positions
        for pos, players in team.items():
            for i, player in enumerate(players):
                # Calculate position based on formation and player index
                x = calculate_position_x(pos, i, len(players))
                y = calculate_position_y(pos)

                # Display player name on the canvas
                self.pitch_canvas.create_text(x, y, text=player["Web name"], fill='white', font=('Moderna', 15, 'bold'))

def calculate_position_x(position, index, total_players):

    if position == 'GK':
        return 450
    elif position == 'DF':
        return (index + 1) * (900 / (total_players + 1))
    elif position == 'MF':
        return (index + 1) * (900 / (total_players + 1))
    elif position == 'FW':
        return (index + 1) * (900 / (total_players + 1))

def calculate_position_y(position):
    if position == 'GK':
        return 430
    elif position == 'DF':
        return 320
    elif position == 'MF':
        return 180
    elif position == 'FW':
        return 90
                

class PlayerCompPage_Head(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Set background color and font style
        self.configure(bg="#f2f2f2")

        # Radio buttons for player positions
        position_frame = tk.Frame(self, bg="#f2f2f2")  # Background color
        position_frame.grid(row=0, column=0, sticky='w', padx=10, pady=30)  # Add padding

        self.position_label = tk.Label(position_frame, text="Select Position:", font=("Arial", 12, "bold"), bg="#f2f2f2")  # Font and background color
        self.position_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)  # Add padding

        self.position_var = tk.StringVar()
        positions = ["DF", "FW", "MF", "GK"]
        for i, position in enumerate(positions):
            tk.Radiobutton(position_frame, text=position, variable=self.position_var, value=position, bg="#f2f2f2").grid(row=0, column=i+1, sticky='w', padx=10, pady=10)  # Add padding

        # Frame for left side dropdowns
        left_frame = tk.LabelFrame(self, bg="#f2f2f2", text = "Player 1")  # Background color
        left_frame.grid(row=1, column=0, padx=130, pady=10, sticky='w')  # Add padding

        # Dropdowns for selecting club and players for left side
        self.club_label_left = tk.Label(left_frame, text="Select Club:", font=("Arial", 12, "bold"), bg="#f2f2f2")  # Font and background color
        self.club_label_left.grid(row=1, column=0, sticky='w', padx=10, pady=10)  # Add padding

        self.club_var_left = tk.StringVar()
        self.club_dropdown_left = ttk.Combobox(left_frame, textvariable=self.club_var_left)
        self.club_dropdown_left.grid(row=1, column=1, sticky='w', padx=10, pady=10)  # Add padding

        self.player_label_left = tk.Label(left_frame, text="Select Player:", font=("Arial", 12, "bold"), bg="#f2f2f2")  # Font and background color
        self.player_label_left.grid(row=2, column=0, sticky='w', padx=10, pady=10)  # Add padding

        self.player_var_left = tk.StringVar()
        self.player_dropdown_left = ttk.Combobox(left_frame, textvariable=self.player_var_left)
        self.player_dropdown_left.grid(row=2, column=1, sticky='w', padx=10, pady=10)  # Add padding

        # Compare button
        compare_button = tk.Button(self, text="Compare", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.compare_players)
        compare_button.grid(row=1, column=1, padx=125, pady=10, sticky='w')  # Place the button in the middle column

        # Frame for right side dropdowns
        right_frame = tk.LabelFrame(self, bg="#f2f2f2", text = "Player 2")  # Background color
        right_frame.grid(row=1, column=2, padx=119, pady=10, sticky='w')  # Add padding

        # Dropdowns for selecting club and players for right side
        self.club_label_right = tk.Label(right_frame, text="Select Club:", font=("Arial", 12, "bold"), bg="#f2f2f2")  # Font and background color
        self.club_label_right.grid(row=1, column=0, sticky='w', padx=10, pady=10)  # Add padding

        self.club_var_right = tk.StringVar()
        self.club_dropdown_right = ttk.Combobox(right_frame, textvariable=self.club_var_right)
        self.club_dropdown_right.grid(row=1, column=1, sticky='w', padx=10, pady=10)  # Add padding

        self.player_label_right = tk.Label(right_frame, text="Select Player:", font=("Arial", 12, "bold"), bg="#f2f2f2")  # Font and background color
        self.player_label_right.grid(row=2, column=0, sticky='w', padx=10, pady=10)  # Add padding

        self.player_var_right = tk.StringVar()
        self.player_dropdown_right = ttk.Combobox(right_frame, textvariable=self.player_var_right)
        self.player_dropdown_right.grid(row=2, column=1, sticky='w', padx=10, pady=10)  # Add padding

        # Load data into club dropdowns
        clubs = list(clubWisePlayerData.keys())
        self.club_dropdown_left['values'] = clubs
        self.club_dropdown_right['values'] = clubs

        # Frame for comparison results
        self.comparison_frame = tk.Frame(self, bg="#f2f2f2")
        self.comparison_frame.grid(row=2, column=1, rowspan=3, columnspan=2, pady=50, sticky='nsew')

        # Function to update player dropdowns based on selected club and position
        def update_player_dropdowns1(*args):
            # Clear the selected values in club and player dropdowns
            self.player_var_left.set("")  # Clear the left player dropdown

            selected_club_left = self.club_var_left.get()
            selected_club_right = self.club_var_right.get()
            selected_position = self.position_var.get()

            values = []

            if selected_club_left and selected_position:
                players_left = clubWisePlayerData.get(selected_club_left, [])
                for player in players_left:
                    if player in positionWisePlayerData.get(selected_position, []):
                        values.append(player)
                self.player_dropdown_left['values'] = values

            values2 = []

            if selected_club_right and selected_position:
                players_right = clubWisePlayerData.get(selected_club_right, [])
                for player in players_right:
                    if player in positionWisePlayerData.get(selected_position, []):
                        values2.append(player)
                self.player_dropdown_right['values'] = values2
        
        def update_player_dropdowns2(*args):
            # Clear the selected values in club and player dropdowns
            self.player_var_right.set("")  # Clear the right player dropdown

            selected_club_left = self.club_var_left.get()
            selected_club_right = self.club_var_right.get()
            selected_position = self.position_var.get()

            values = []

            if selected_club_left and selected_position:
                players_left = clubWisePlayerData.get(selected_club_left, [])
                for player in players_left:
                    if player in positionWisePlayerData.get(selected_position, []):
                        values.append(player)
                self.player_dropdown_left['values'] = values

            values2 = []

            if selected_club_right and selected_position:
                players_right = clubWisePlayerData.get(selected_club_right, [])
                for player in players_right:
                    if player in positionWisePlayerData.get(selected_position, []):
                        values2.append(player)
                self.player_dropdown_right['values'] = values2

        def update_player_dropdowns3(*args):
            # Clear the selected values in club and player dropdowns
            self.player_var_left.set("")  # Clear the left player dropdown
            self.player_var_right.set("")  # Clear the right player dropdown

            selected_club_left = self.club_var_left.get()
            selected_club_right = self.club_var_right.get()
            selected_position = self.position_var.get()

            values = []

            if selected_club_left and selected_position:
                players_left = clubWisePlayerData.get(selected_club_left, [])
                for player in players_left:
                    if player in positionWisePlayerData.get(selected_position, []):
                        values.append(player)
                self.player_dropdown_left['values'] = values

            values2 = []

            if selected_club_right and selected_position:
                players_right = clubWisePlayerData.get(selected_club_right, [])
                for player in players_right:
                    if player in positionWisePlayerData.get(selected_position, []):
                        values2.append(player)
                self.player_dropdown_right['values'] = values2

        # Bind the update function to club and position dropdowns
        self.club_var_left.trace('w', update_player_dropdowns1)
        self.club_var_right.trace('w', update_player_dropdowns2)
        self.position_var.trace('w', update_player_dropdowns3)

        # Set default values for dropdowns
        self.club_var_left.set(clubs[0])
        self.club_var_right.set(clubs[0])
        self.position_var.set(positions[0])

        # Adjust grid weights to make the layout expandable
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def compare_players(self):
        selected_left_player = self.player_var_left.get()
        selected_right_player = self.player_var_right.get()

        left_player_data = {}
        right_player_data = {}
        for item in players_statistics:
            if (item["Name"] == selected_left_player):
                left_player_data = item
            if (item["Name"] == selected_right_player):
                right_player_data = item

        # Clear previous comparison results
        for widget in self.comparison_frame.winfo_children():
            widget.destroy()

        # Create a treeview to display the comparison results in a table
        columns = [selected_left_player, "Metric", selected_right_player]
        tree = ttk.Treeview(self.comparison_frame, columns=columns, show="headings")
        tree.heading(selected_left_player, text=left_player_data ["Web name"], anchor='center')
        tree.heading("Metric", text="Metric", anchor='center')
        tree.heading(selected_right_player, text=right_player_data ["Web name"], anchor='center')

        # Add data to the treeview
        if self.position_var.get() == "FW":
            metrics = ["Minutes", "Goals", "Assists", "Penalties missed", "Yellow cards", "Red cards", "Starts", "xG", "xA"]
        if self.position_var.get() == "MF":
            metrics = ["Minutes", "Goals", "Assists", "Penalties missed", "Yellow cards", "Red cards", "Starts", "xG", "xA"]
        if self.position_var.get() == "DF":
            metrics = ["Minutes", "Goals", "Assists", "Clean sheets", "Goals conceded", "Yellow cards", "Red cards", "Starts",  "Expected goals conceded", "Expected goal involvements"]
        if self.position_var.get() == "GK":
            metrics = ["Minutes", "Clean sheets", "Goals conceded", "Penalties saved", "Yellow cards", "Red cards", "Saves", "Starts", "Expected goals conceded"]
        for metric in metrics:
            left_value = left_player_data.get(metric, "-")
            right_value = right_player_data.get(metric, "-")
            tree.insert("", "end", values=[left_value, metric, right_value], tags=('centered',))

        # Center the cell contents
        tree.tag_configure('centered', anchor='center')

        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        tree.grid(row=0, column=0, sticky='w', pady=10)

class PlayerCompPage_Form(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set background color and font style
        self.configure(bg="#f2f2f2")

        # Radio buttons for player positions
        position_frame = tk.Frame(self, bg="#f2f2f2")  # Background color
        position_frame.grid(row=0, column=0, sticky='w', padx=10, pady=30)  # Add padding

        self.position_label = tk.Label(position_frame, text="Select Position:", font=("Arial", 12, "bold"), bg="#f2f2f2")  # Font and background color
        self.position_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)  # Add padding

        self.position_var = tk.StringVar()
        positions = ["DF", "FW", "MF", "GK"]
        for i, position in enumerate(positions):
            tk.Radiobutton(position_frame, text=position, variable=self.position_var, value=position, bg="#f2f2f2", command=self.update_treeview).grid(row=0, column=i+1, sticky='w', padx=10, pady=10)  # Add padding

        # Treeview widget for displaying player data
        self.tree = ttk.Treeview(self, columns=("Player", "Form Rating", "Current Cost"), show="headings", height=30)  # Adjust height here
        self.tree.heading("Player", text="Player", anchor="center")
        self.tree.heading("Form Rating", text="Form rating", anchor="center")
        self.tree.heading("Current Cost", text="Current cost", anchor="center")
        self.tree.column("Player", width=300, anchor="center")  # Adjust width of Player column
        self.tree.column("Form Rating", width=250, anchor="center")  # Adjust width of Form Rating column
        self.tree.column("Current Cost", width=250, anchor="center")
        self.tree.grid(row=1, column=2, padx=50, pady=10, sticky='nsew')  # Center-align the table within the main frame

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        # Make a copy of players_statistics to avoid modifying the original list
        sorted_players = players_statistics.copy()

        # Perform merge sort
        self.merge_sort(sorted_players)

        # Insert sorted players into the treeview
        for item in sorted_players:
            position_key = self.position_var.get()
            if item["Name"] in positionWisePlayerData[position_key]:
                self.tree.insert("", "end", values=(item["Name"], item["Relative form rating"], int(item["Current cost"])/10))

    def merge_sort(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i]["Relative form rating"] >= right_half[j]["Relative form rating"]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1


class PlayersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="")
        label.pack(padx=10, pady=0)

        # Create a frame to hold radio buttons, labels, and text fields
        self.criteria_frame = tk.Frame(self)
        self.criteria_frame.pack(padx=20, pady=20, anchor="w")

        s1 = '{: <18}'.format("Choose filter:")
        
        # Create a label for the filter criteria
        filter_label = tk.Label(self.criteria_frame, text=s1, font='Helvetica 18 bold')
        filter_label.grid(row=0, column=0, sticky="w")

        s2 = '{: <6}'.format("")
        s3 = '{: <6}'.format("")

        # Create radio buttons for filter criteria
        self.criteria_var = tk.StringVar(value="")
        club_radio = ct.CTkRadioButton(self.criteria_frame, text="Club", variable=self.criteria_var, value="club", font=ct.CTkFont(family="Helvetica", size=17))
        fake_label = tk.Label(self.criteria_frame, text=s2)
        fake_label2 = tk.Label(self.criteria_frame, text=s3)
        fake_label3 = tk.Label(self.criteria_frame, text=s3)
        position_radio = ct.CTkRadioButton(self.criteria_frame, text="Position", variable=self.criteria_var, value="position", font=ct.CTkFont(family="Helvetica", size=17))

        club_radio.grid(row=0, column=1, sticky="w")
        position_radio.grid(row=2, column=1, sticky="w", pady = 10)
        fake_label.grid(row=0, column = 5, sticky="w")
        fake_label3.grid(row=0, column = 2, sticky="w")
        fake_label2.grid(row=0, column = 7, sticky="w")

        # Create a dynamic combo box for user input 
        n = tk.StringVar()
        self.filter_combobox = ttk.Combobox(self.criteria_frame, width=20, textvariable=n)
        self.filter_combobox.grid(row=0, column=4, sticky="w")

        self.criteria_var.trace("w", self.update_combobox_options)

        club_radio.bind("<ButtonRelease-1>", self.update_combobox_options)
        position_radio.bind("<ButtonRelease-1>", self.update_combobox_options)

        # Create a button to apply the filter
        apply_filter_button = ct.CTkButton(self.criteria_frame, text="Apply", command=self.apply_filter, width=100) 
        apply_filter_button.grid(row=0, column=6, sticky="w")

        # Create a button to apply the filter
        clear_filter_button = ct.CTkButton(self.criteria_frame, text="Clear", command=self.clear_filter, width=100)
        clear_filter_button.grid(row=0, column=8, sticky="w")

        # Create a Treeview widget for displaying player information
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("Name", "Position", "Club")

        # Define column headings with center alignment
        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Position", text="Position", anchor=tk.CENTER)
        self.tree.heading("Club", text="Club", anchor=tk.CENTER)

        # Configure column widths
        self.tree.column("#0", width=0, stretch=tk.NO)  # Invisible column for treeview indicator
        self.tree.column("Name", width=150, anchor=tk.CENTER)
        self.tree.column("Position", width=100, anchor=tk.CENTER)
        self.tree.column("Club", width=100, anchor=tk.CENTER)

        for player in players_data:
            self.tree.insert("", "end", values=(player["name"], player["position"], player["club"]))

        self.tree.pack(expand=True, fill=tk.BOTH)

    def update_combobox_options(self, *args):
        selected_criteria = self.criteria_var.get()
        if selected_criteria == "club":
            self.filter_combobox['values'] = clubs
        elif selected_criteria == "position":
            self.filter_combobox['values'] = positions

        # Clear the selected value in the Combobox
        self.filter_combobox.set("")
    
    def clear_filter (self):
        for child in self.criteria_frame.winfo_children():
            if isinstance(child, ct.CTkRadioButton): 
                child.deselect()

        for record in self.tree.get_children():
            self.tree.delete(record)

        for player in players_data:
            self.tree.insert("", "end", values=(player["name"], player["position"], player["club"]))

    def apply_filter(self):
        # Get the selected filter criteria and user input
        selected_criteria = self.criteria_var.get()
        user_input = self.filter_combobox.get().lower() # Convert user input to lowercase for case-insensitive comparison

        # Filter players based on the selected criteria and user input
        filtered_players = [player for player in players_data if user_input in player[selected_criteria].lower()]

        # Clear the Treeview
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Populate the Treeview with filtered player information
        for player in filtered_players:
            self.tree.insert("", "end", values=(player["name"], player["position"], player["club"]))

        # Update the view
        self.tree.update()

class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("FPL Guru")
        self.geometry("1500x800")

        container = tk.Frame(self, height=1500, width=800)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, MyTeamPage_Pitch, PlayerCompPage_Head, PlayerCompPage_Form, PlayersPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
if __name__ == "__main__":
    testObj = Windows()
    testObj.mainloop()
