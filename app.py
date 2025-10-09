import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# EPL team stats (simplified example)
team_stats = {
    "Arsenal": {"attack": 85, "defense": 75, "form": [3,3,1,3,0], "top_scorer": "Saka"},
    "Manchester City": {"attack": 90, "defense": 85, "form": [3,3,3,3,1], "top_scorer": "Haaland"},
    "Liverpool": {"attack": 88, "defense": 80, "form": [3,1,3,3,0], "top_scorer": "Foden"},
    "Chelsea": {"attack": 82, "defense": 78, "form": [1,3,0,3,3], "top_scorer": "Havertz"},
    "Manchester United": {"attack": 80, "defense": 76, "form": [3,0,3,1,3], "top_scorer": "Rashford"},
    "Tottenham": {"attack": 81, "defense": 77, "form": [1,3,0,3,3], "top_scorer": "Kane"},
    "Newcastle": {"attack": 78, "defense": 74, "form": [3,3,1,0,3], "top_scorer": "Wilson"},
    "Brighton": {"attack": 76, "defense": 72, "form": [0,3,3,1,1], "top_scorer": "Mitoma"},
    # Add remaining EPL teams here
}

def calculate_team_strength(team):
    attack = team_stats[team]["attack"]
    defense = team_stats[team]["defense"]
    form = np.mean(team_stats[team]["form"])
    return attack*0.6 + defense*0.3 + form*5

def simulate_match(home_team, away_team, simulations=5000):
    home_adv = 1.1
    home_strength = calculate_team_strength(home_team) * home_adv
    away_strength = calculate_team_strength(away_team)

    home_goals_list, away_goals_list = [], []
    home_scorer_goals, away_scorer_goals = {}, {}

    for _ in range(simulations):
        home_exp = max(home_strength / away_strength * 1.5, 0.1)
        away_exp = max(away_strength / home_strength * 1.0, 0.1)

        home_goals = np.random.poisson(home_exp)
        away_goals = np.random.poisson(away_exp)
        home_goals_list.append(home_goals)
        away_goals_list.append(away_goals)

        # Top scorer simulation
        if home_goals > 0:
            home_scorer_goals[team_stats[home_team]["top_scorer"]] = home_scorer_goals.get(team_stats[home_team]["top_scorer"],0) + np.random.binomial(home_goals,0.4)
        if away_goals > 0:
            away_scorer_goals[team_stats[away_team]["top_scorer"]] = away_scorer_goals.get(team_stats[away_team]["top_scorer"],0) + np.random.binomial(away_goals,0.4)

    home_wins = sum(h>a for h,a in zip(home_goals_list,away_goals_list)) / simulations
    draws = sum(h==a for h,a in zip(home_goals_list,away_goals_list)) / simulations
    away_wins = sum(h<a for h,a in zip(home_goals_list,away_goals_list)) / simulations

    avg_home_goals = np.mean(home_goals_list)
    avg_away_goals = np.mean(away_goals_list)

    total_goals = sum(home_goals_list)+sum(away_goals_list)
    top_scorer_probs = {}
    for scorer, goals in {**home_scorer_goals, **away_scorer_goals}.items():
        top_scorer_probs[scorer] = round((goals/total_goals)*100,2) if total_goals>0 else 0

    return {
        "home_team": home_team,
        "away_team": away_team,
        "avg_home_goals": round(avg_home_goals,2),
        "avg_away_goals": round(avg_away_goals,2),
        "home_win_prob": round(home_wins*100,2),
        "draw_prob": round(draws*100,2),
        "away_win_prob": round(away_wins*100,2),
        "top_scorer_probs": top_scorer_probs
    }

def plot_prediction(prediction):
    # Outcome probabilities
    fig, ax = plt.subplots(figsize=(8,4))
    labels = [f'{prediction["home_team"]} Win','Draw',f'{prediction["away_team"]} Win']
    probs = [prediction["home_win_prob"], prediction["draw_prob"], prediction["away_win_prob"]]
    colors = ['green','gray','red']
    ax.bar(labels, probs, color=colors)
    ax.set_ylim(0,100)
    ax.set_ylabel("Probability (%)")
    ax.set_title("Match Outcome Probabilities")
    st.pyplot(fig)

    # Top scorers
    if prediction["top_scorer_probs"]:
        fig2, ax2 = plt.subplots(figsize=(8,4))
        scorers = list(prediction["top_scorer_probs"].keys())
        goals_prob = list(prediction["top_scorer_probs"].values())
        ax2.bar(scorers, goals_prob, color='blue')
        ax2.set_ylabel("Probability (%)")
        ax2.set_title("Top Scorer Probabilities")
        st.pyplot(fig2)

# Streamlit App
st.title("EPL Match Predictor")
teams = list(team_stats.keys())
home_team = st.selectbox("Select Home Team", teams)
away_team = st.selectbox("Select Away Team", [t for t in teams if t != home_team])

if st.button("Predict Match"):
    prediction = simulate_match(home_team, away_team)
    st.write(f"**Average Score:** {home_team} {prediction['avg_home_goals']} - {prediction['avg_away_goals']} {away_team}")
    st.write(f"**Win/Draw Probabilities:** Home Win: {prediction['home_win_prob']}%, Draw: {prediction['draw_prob']}%, Away Win: {prediction['away_win_prob']}%")
    if prediction["top_scorer_probs"]:
        st.write("**Top Scorer Probabilities:**")
        for scorer, prob in prediction["top_scorer_probs"].items():
            st.write(f"{scorer}: {prob}%")
    plot_prediction(prediction)
