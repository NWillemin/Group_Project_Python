#first, import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

#read the URL of the dataset(CSV) using pandas
url = 'https://data.sihf.ch/Statistic/api/cms/export?alias=player&searchQuery=1%2F%2F1&filterQuery=&filterBy=Season%2CPhase%2CTeam%2CPosition%2CLicence&orderBy=points&orderByDescending=true&format=csv'
stats = pd.read_csv(url, sep = ';')

#set a first dictionary to translate the values of the column "Pos"
dictionary_val = {'Stürmer':'Forward', 'Verteidiger':'Defender'}
#2nd dictionary for the columns (this way, we avoid replacing the 'R' of 'Rapperswil' with 'Ranking')
dictionary_col = {"Spieler":"Player", "R":"Ranking"}

#apply the first dictionary to the values
stats.replace(dictionary_val, inplace = True, regex = True)
#apply the second dictionary to the columns
stats.rename(columns = dictionary_col, inplace = True)
#delete an uncessary column
del stats["+/-"]
#create 3 new columns
#the first one rounds up to two decimal numbers the penalty time per game 
stats["PIM/GP"] = round(stats["PIM Total"] / stats["GP"], 2)
#the second is the efficiency of the player (number of points per game minus penalty time)
stats["Eff Total"] = stats["PTS"] - stats["PIM Total"]
stats["Eff/GP"] = stats["P/GP"] - stats["PIM/GP"]

#set 'Ranking' as the index
stats.set_index("Ranking", inplace = True)

print("This program allows you to navigate through the statistics of the National League, Switzerland's elite ice hockey league. You can search by 'player', 'ranking', 'team', 'team rankings', 'top rankings', 'defenders', 'goals', 'assists', 'efficiency', and 'penalties'. Enjoy!")
#set the start_over variable as "yes" to enter the loop
start_over = "yes"

#start the loop 
while start_over == "yes":
    #criterion is the user's search
    criterion = input("Search by: ").lower()
    
    #all possible criteria are used with the "if" function
    if criterion == "player":
        #asking for the player's name
        player_name = input("Enter Player's Name: ")
        #defining the data we will use for the bar chart
        player_stats = stats.loc[stats["Player"] == player_name, ["GP", "G", "A", "PTS", "PIM Total"]]
        #if function to be able to detect an incorrect input
        if not player_stats.empty:
            #first, returning all stats of the player
            print(stats.loc[stats["Player"] == player_name, :])
            #then, plotting the bar chart using seaborn
            #transforming the dataframe into a series 
            player_stats = player_stats.iloc[0]
            #configuring the plot
            #seaborn theme whitegrid for better visibility
            sns.set_theme(style="whitegrid")  
            plt.figure(figsize=(10, 6))
            sns.barplot(x=player_stats.index, y=player_stats.values)
            #rotating the x values for style
            plt.xticks(rotation=45)
            plt.title(f'Statistics for {player_name}')
            plt.xlabel('Statistical Categories')
            plt.ylabel('Values')
            plt.show()
        #error message if player's name doesn't match
        else:
            print("Player not found. Please enter the last and first name of the player (e.g., 'Carr Daniel')")

    #return the stats of the player corresponding to the inserted ranking
    elif criterion == "ranking":
        try:
            rank = int(input("Enter Ranking: "))
            # check if the entered ranking is within the range of the DataFrame
            while rank > len(stats):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(stats)}")
                rank = int(input("And how many players do you want to display? "))
            print(stats.iloc[rank-1])
        except ValueError:
            # handle the case where the input is not an integer
            print("Invalid input. Please enter an integer.")
        
    #return a list of all the players of a team with their respective points
    elif criterion == "team":
        team_name = input("Enter Team's Name: ")
        team_stats = stats.loc[stats["Team"] == team_name, ["Player", "PTS"]]
        if not team_stats.empty:
            print(team_stats)
        else:
            print("Team not found. Please enter the team's full name (e.g., 'Fribourg-Gottéron'). Search for the stat 'team rankings' to see every team's full name.")
    
    elif criterion == "team rankings":
        #new dataframe Teams with their stats summed up
        Teams = stats.groupby("Team").sum()
        #creating a ranking 
        Teams = Teams.sort_values(by = 'PTS', ascending = False)
        #returning the teams' relevant stats
        print(Teams.loc[:, ["G", "A", "PTS", "PIM Total", "Eff Total"]])
        #configuring the plot
        sns.set_theme(style="whitegrid")
        #bigger size than for the players since more bars
        plt.figure(figsize=(15, 8))
        sns.barplot(x=Teams.index, y="PTS", data=Teams)
        #rotating the x values by 90 degrees since some teams' names are very long
        plt.xticks(rotation=90)
        plt.title("Total Points by Team")
        plt.xlabel("Team")
        plt.ylabel("Total Points")
        plt.show()
        
    #return the top N players 
    elif criterion == "top rankings":
        #proposing 2 different rankings
        choice = input("Insert 'a' for the ranking by total points and 'b' for the ranking by points per game.").lower()
        #loop for a potential invalid response
        while choice != "a" and choice != "b": 
            print("Invalid input. Please answer with 'a' or 'b'.")
            choice = input("Insert 'a' for the ranking by total points and 'b' for the ranking by points per game.").lower()
        #function to handle an invalid entry
        try:
            N = int(input("And how many players do you want to display? "))
            while N > len(stats):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(stats)}")
                N = int(input("And how many players do you want to display? "))
            #define the ranking for either the total points (initial ranking) or the points per game
            if choice == "a":
                print(stats.head(N))
            elif choice == "b":
                pgp_ranking = stats.sort_values(by = "P/GP", ascending = False)
                print(pgp_ranking.head(N))
        except ValueError: 
            print("Invalid input. Please enter an integer.")
        
    #return the top N defenders
    elif criterion == "defenders":
        def_ranking = stats[stats["Pos"] == "Defender"]
        try:
            N = int(input("How many defenders do you want to display? "))
            while N > len(def_ranking):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(def_ranking)}")
                N = int(input("How many defenders do you want to display? "))
            print(def_ranking.head(N))
        except ValueError: 
            print("Invalid input. Please enter an integer.")
        
        
    #return the top N goal scorers
    elif criterion == "goals":
        g_ranking = stats.sort_values(by = "G", ascending = False)
        try:
            N = int(input("How many players do you want to display? "))
            while N > len(stats):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(stats)}")
                N = int(input("How many players do you want to display? "))
            print(g_ranking.head(N))
        except ValueError: 
            print("Invalid input. Please enter an integer.")
        
    #return the top N assisters
    elif criterion == "assists":
        a_ranking = stats.sort_values(by = "A", ascending = False)
        try:
            N = int(input("How many players do you want to display? "))
            while N > len(stats):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(stats)}")
                N = int(input("And how many players do you want to display? "))
            print(a_ranking.head(N))
        except ValueError: 
            print("Invalid input. Please enter an integer.")
        
    #return the top N most efficient players (same concept as with the "top ranking" criterion)
    elif criterion == "efficiency":
        choice = input("Insert 'a' for the ranking by total efficiency and 'b' for the ranking by efficiency per game.").lower()
        while choice != "a" and choice != "b": 
            print("Invalid response. Please answer with 'a' or 'b'.")
            choice = input("Insert 'a' for the ranking by total efficiency and 'b' for the ranking by efficiency per game.").lower()
        if choice == "a":
            eff_ranking = stats.sort_values(by = "Eff Total", ascending = False)
        elif choice == "b":
            eff_ranking = stats.sort_values(by = "Eff/GP", ascending = False)
        try:
            N = int(input("And how many players do you want to display? "))
            while N > len(stats):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(stats)}")
                N = int(input("How many players do you want to display? "))
            print(eff_ranking.head(N))
        except ValueError: 
            print("Invalid input. Please enter an integer.")
            
    
    #return the top N players with most penalties (same concept as with the "top ranking" criterion)
    elif criterion == "penalties":
        choice = input("Insert 'a' for the ranking by total penalties and 'b' for the ranking by penalties per game.").lower()
        while choice != "a" and choice != "b": 
            print("Invalid response. Please answer with 'a' or 'b'.")
            choice = input("Insert 'a' for the ranking by total penalties and 'b' for the ranking by penalties per game.").lower()
        if choice == "a":
            pim_ranking = stats.sort_values(by = "PIM Total", ascending = False)
        elif choice == "b":
            pim_ranking = stats.sort_values(by = "PIM/GP", ascending = False)
        try:
            N = int(input("And how many players do you want to display? "))
            while N > len(stats):
                print(f"Invalid input. Please make sure to write a number between 1 and {len(stats)}")
                N = int(input("How many players do you want to display? "))
            print(pim_ranking.head(N))
        except ValueError: 
            print("Invalid input. Please enter an integer.")
    
    #explain the possible stats the user can search if his initial entry is invalid
    else:
        print("Invalid search. Please enter one of the following: 'player', 'ranking', 'team', 'team rankings', 'top rankings', 'defenders', 'goals', 'assists', 'efficiency', 'penalties'.")
    
    #ask if the user wants to restart the loop    
    start_over = input("Would you like to look for other stats? ").lower()
    
    #new loop to make sure the user's answer is correct ('yes' or 'no')
    while start_over != "yes" and start_over != "no":
        print("Invalid response. Please answer with 'yes' or 'no'.")
        start_over = input("Would you like to look for other stats? ").lower()
        
    #print a message depending on the user's answer
    if start_over == "yes":
        print("Let's start over then!")
    elif start_over == "no":
        print("I hope you found the stats you were looking for!")
