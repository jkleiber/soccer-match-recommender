import requests
import json
from pprint import pprint
from operator import itemgetter
import math

BLOWOUT_FACTOR = 1.55 #Experimentally determined by plugging A^(goal difference) into google calc until it looked right
IMPORTANCE_CONSTANT = 1.5
UPSET_GD_MULTIPLIER = 2
UPSET_VALUE_EXP = 1.75 #Also experimentally determined by google calc using (ranking diff)^X until satisfactory

def get_arbitrary_team_rankings():
    rankings = []
    rankings.append("United States")
    rankings.append("France")
    rankings.append("Canada")
    rankings.append("Italy")
    rankings.append("Germany")
    rankings.append("England")
    rankings.append("Netherlands")
    rankings.append("Japan")
    rankings.append("Sweden")
    rankings.append("Spain")
    rankings.append("China PR")
    rankings.append("Australia")
    rankings.append("Brazil")
    rankings.append("Norway")
    rankings.append("Argentina")
    rankings.append("Nigeria")
    rankings.append("Chile")
    rankings.append("Jamaica")
    rankings.append("Cameroon")
    rankings.append("New Zealand")
    rankings.append("Scotland")
    rankings.append("South Africa")
    rankings.append("South Korea")
    rankings.append("Thailand") 

    return rankings

def get_matchup_disparity(team_a, team_b):
    a = 0
    b = 0
    disp = 0
    rankings = get_arbitrary_team_rankings()
    for i in range(0, len(rankings)):
        if rankings[i] == team_a:
            a = i + 1
        elif rankings[i] == team_b:
            b = i + 1

        if a != 0 and b != 0:
            break
    
    disp = abs(a - b)
    return [disp, a, b]

def calculate_upset(team_a, team_b, team_A_win):
    comp_teams = get_matchup_disparity(team_a, team_b)
    upset = 0
    is_upset = False
    if (team_A_win == True and comp_teams[1] < comp_teams[2]) or (team_A_win == False and comp_teams[2] < comp_teams[1]):
        upset = 0
    else:
        upset = comp_teams[0] ** UPSET_VALUE_EXP
        is_upset = True

    return [upset, is_upset]

def calculate_importance(team_a, team_b):
    comp_teams = get_matchup_disparity(team_a, team_b)
    avg_rank = ((33 - comp_teams[1]) + (33 - comp_teams[2])) / 2
    offset = min((33 - comp_teams[1]), (33 - comp_teams[2]))
    return avg_rank + offset

def calculate_suspense(events):
    pass

#World cup API on HackerNews: https://news.ycombinator.com/item?id=17310483
todays_match_url = "http://worldcup.sfg.io/matches/today"

#Get the JSON data from the API
response = requests.get(todays_match_url)
match_data = response.json()

#Store match results in a dict
matches = {}

#Run through each match
for i in range(0, len(match_data)):
    #'Away' team metrics
    away_team_name   = match_data[i]['away_team']['country']
    away_team_goals  = match_data[i]['away_team']['goals']
    away_team_events = match_data[i]['away_team_events'][0]

    #'Home' team metrics
    home_team_name   = match_data[i]['home_team']['country']
    home_team_goals  = match_data[i]['home_team']['goals']
    home_team_events = match_data[i]['home_team_events'][0]

    #Name the match
    key = home_team_name + " vs. " + away_team_name

    """
    Stats to determine the watchability of the game
    """
    #points - each game has a points score that tells how good it was
    points = 0

    #Total Goals (More is better)
    total_goals = home_team_goals + away_team_goals

    #Was this match an upset?
    upset_list  = calculate_upset(home_team_name, away_team_name, home_team_goals > away_team_goals)
    upset_score = upset_list[0]
    is_upset    = upset_list[1]

    #Goal Difference and Upset Score (+ some adjustments)
    goal_difference = abs(home_team_goals - away_team_goals)
    if is_upset == True:
        goal_difference *= UPSET_GD_MULTIPLIER
    else:
        upset_score = BLOWOUT_FACTOR ** goal_difference
        
    #Determine how important a match is based on ranking of teams in the match
    match_importance = calculate_importance(home_team_name, away_team_name) * IMPORTANCE_CONSTANT

    #Calculate suspense by looking to see how many late goals there were
    #home_susp = calculate_suspense(home_team_events)
    #away_susp = calculate_suspense(away_team_events)
    #total_suspense = home_susp + away_susp

    #Calculate the value of watching this match
    points = total_goals + match_importance + upset_score # + total_suspense
    matches[key] = points

#Print match ranking results
i = 1
for (k, v) in sorted(matches.items(), key = itemgetter(1), reverse = True):
    print(str(i) + ". " + str(k))
    i += 1
