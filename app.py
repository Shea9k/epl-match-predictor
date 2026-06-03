import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import combinations
 
# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EPL Match Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}
 
h1, h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }
 
.stApp { background-color: #0d1117; }
 
.metric-card {
    background: linear-gradient(135deg, #161b22, #21262d);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 6px 0;
}
.metric-card .value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
}
.metric-card .label {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}
.green  { color: #3fb950; }
.gray   { color: #8b949e; }
.red    { color: #f85149; }
.gold   { color: #d29922; }
 
.vs-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    text-align: center;
    letter-spacing: 4px;
    padding: 10px 0;
    background: linear-gradient(90deg, #3fb950, #58a6ff, #f85149);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
 
.form-dot {
    display: inline-block;
    width: 14px; height: 14px;
    border-radius: 50%;
    margin: 2px;
}
 
div[data-testid="stSelectbox"] label { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }
div[data-testid="stButton"] button {
    background: linear-gradient(90deg, #238636, #2ea043);
    color: white;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 2px;
    border: none;
    border-radius: 8px;
    padding: 12px 40px;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
}
div[data-testid="stButton"] button:hover { opacity: 0.85; }
 
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 2px;
    border-bottom: 2px solid #30363d;
    padding-bottom: 6px;
    margin: 24px 0 16px;
    color: #58a6ff;
}
</style>
""", unsafe_allow_html=True)
 
# ── Team data (all 20 EPL teams, 2024-25 season approximations) ─────────────────
team_stats = {
    "Arsenal": {
        "attack": 85, "defense": 80, "form": [3,3,1,3,3],
        "top_scorer": "Saka", "badge": "🔴"
    },
    "Manchester City": {
        "attack": 90, "defense": 85, "form": [3,3,3,1,3],
        "top_scorer": "Haaland", "badge": "🔵"
    },
    "Liverpool": {
        "attack": 88, "defense": 82, "form": [3,3,3,1,3],
        "top_scorer": "Salah", "badge": "🔴"
    },
    "Chelsea": {
        "attack": 82, "defense": 76, "form": [1,3,0,3,3],
        "top_scorer": "Palmer", "badge": "🔵"
    },
    "Manchester United": {
        "attack": 76, "defense": 70, "form": [1,0,3,1,0],
        "top_scorer": "Rashford", "badge": "🔴"
    },
    "Tottenham": {
        "attack": 79, "defense": 72, "form": [3,0,1,3,1],
        "top_scorer": "Son", "badge": "⚪"
    },
    "Newcastle United": {
        "attack": 78, "defense": 77, "form": [3,1,3,0,3],
        "top_scorer": "Isak", "badge": "⚫"
    },
    "Brighton": {
        "attack": 77, "defense": 74, "form": [1,3,3,0,1],
        "top_scorer": "Welbeck", "badge": "🔵"
    },
    "Aston Villa": {
        "attack": 82, "defense": 77, "form": [3,3,1,3,0],
        "top_scorer": "Watkins", "badge": "🟣"
    },
    "West Ham": {
        "attack": 73, "defense": 70, "form": [0,1,3,0,3],
        "top_scorer": "Bowen", "badge": "🔵"
    },
    "Wolves": {
        "attack": 68, "defense": 69, "form": [0,1,0,3,1],
        "top_scorer": "Cunha", "badge": "🟠"
    },
    "Fulham": {
        "attack": 74, "defense": 72, "form": [3,1,3,1,0],
        "top_scorer": "Jimenez", "badge": "⚪"
    },
    "Brentford": {
        "attack": 75, "defense": 71, "form": [3,0,1,3,1],
        "top_scorer": "Mbeumo", "badge": "🔴"
    },
    "Crystal Palace": {
        "attack": 70, "defense": 71, "form": [1,0,3,1,1],
        "top_scorer": "Eze", "badge": "🔴"
    },
    "Everton": {
        "attack": 65, "defense": 68, "form": [1,1,0,1,3],
        "top_scorer": "Calvert-Lewin", "badge": "🔵"
    },
    "Nottingham Forest": {
        "attack": 72, "defense": 75, "form": [3,1,0,3,1],
        "top_scorer": "Awoniyi", "badge": "🔴"
    },
    "Bournemouth": {
        "attack": 71, "defense": 67, "form": [3,1,1,0,3],
        "top_scorer": "Kluivert", "badge": "🔴"
    },
    "Leicester City": {
        "attack": 67, "defense": 62, "form": [0,0,1,0,1],
        "top_scorer": "Vardy", "badge": "🔵"
    },
    "Ipswich Town": {
        "attack": 62, "defense": 60, "form": [0,1,0,0,1],
        "top_scorer": "Broadhead", "badge": "🔵"
    },
    "Southampton": {
        "attack": 58, "defense": 55, "form": [0,0,0,1,0],
        "top_scorer": "Archer", "badge": "🔴"
    },
}
 
# ── Helper functions ────────────────────────────────────────────────────────────
 
def form_points(team: str) -> float:
    """Average points from last 5 games (0=loss, 1=draw, 3=win)."""
    return np.mean(team_stats[team]["form"])
 
def calculate_team_strength(team: str) -> float:
    atk   = team_stats[team]["attack"]
    defn  = team_stats[team]["defense"]
    form  = form_points(team)
    return atk * 0.55 + defn * 0.30 + form * 6
 
def expected_goals(home_team: str, away_team: str):
    """Return (home_xG, away_xG) using attack vs opponent defence."""
    h_atk  = team_stats[home_team]["attack"]
    h_def  = team_stats[home_team]["defense"]
    a_atk  = team_stats[away_team]["attack"]
    a_def  = team_stats[away_team]["defense"]
    h_form = form_points(home_team)
    a_form = form_points(away_team)
 
    HOME_ADVANTAGE = 1.12
    BASE_GOALS     = 1.35
 
    home_xg = BASE_GOALS * (h_atk / 80) * (80 / a_def) * HOME_ADVANTAGE * (1 + (h_form - 1.5) * 0.06)
    away_xg = BASE_GOALS * (a_atk / 80) * (80 / h_def)                  * (1 + (a_form - 1.5) * 0.06)
 
    return max(home_xg, 0.2), max(away_xg, 0.2)
 
def simulate_match(home_team: str, away_team: str, simulations: int = 10_000) -> dict:
    home_xg, away_xg = expected_goals(home_team, away_team)
 
    rng = np.random.default_rng()
    home_goals_arr = rng.poisson(home_xg, simulations)
    away_goals_arr = rng.poisson(away_xg, simulations)
 
    home_wins = int(np.sum(home_goals_arr > away_goals_arr))
    draws     = int(np.sum(home_goals_arr == away_goals_arr))
    away_wins = int(np.sum(home_goals_arr < away_goals_arr))
 
    # Score probability map (top 6x6 grid)
    score_probs = {}
    for hg in range(7):
        for ag in range(7):
            p = np.sum((home_goals_arr == hg) & (away_goals_arr == ag)) / simulations
            if p > 0.001:
                score_probs[f"{hg}-{ag}"] = round(p * 100, 2)
    top_scores = dict(sorted(score_probs.items(), key=lambda x: -x[1])[:8])
 
    # Top scorer simulation
    home_scorer = team_stats[home_team]["top_scorer"]
    away_scorer = team_stats[away_team]["top_scorer"]
 
    h_scorer_goals = int(np.sum(rng.binomial(np.maximum(home_goals_arr, 0), 0.38)))
    a_scorer_goals = int(np.sum(rng.binomial(np.maximum(away_goals_arr, 0), 0.38)))
    total = h_scorer_goals + a_scorer_goals
 
    top_scorer_probs = {}
    if total > 0:
        top_scorer_probs[home_scorer] = round(h_scorer_goals / total * 100, 1)
        top_scorer_probs[away_scorer] = round(a_scorer_goals / total * 100, 1)
 
    # BTTS / Over 2.5
    btts       = round(np.mean((home_goals_arr > 0) & (away_goals_arr > 0)) * 100, 1)
    over_2_5   = round(np.mean((home_goals_arr + away_goals_arr) > 2.5) * 100, 1)
    clean_home = round(np.mean(away_goals_arr == 0) * 100, 1)
    clean_away = round(np.mean(home_goals_arr == 0) * 100, 1)
 
    return {
        "home_team":       home_team,
        "away_team":       away_team,
        "home_xg":         round(home_xg, 2),
        "away_xg":         round(away_xg, 2),
        "avg_home_goals":  round(float(np.mean(home_goals_arr)), 2),
        "avg_away_goals":  round(float(np.mean(away_goals_arr)), 2),
        "home_win_prob":   round(home_wins / simulations * 100, 1),
        "draw_prob":       round(draws     / simulations * 100, 1),
        "away_win_prob":   round(away_wins / simulations * 100, 1),
        "top_scorer_probs": top_scorer_probs,
        "top_scores":      top_scores,
        "btts":            btts,
        "over_2_5":        over_2_5,
        "clean_home":      clean_home,
        "clean_away":      clean_away,
    }
 
# ── Plotting ────────────────────────────────────────────────────────────────────
 
def dark_style():
    plt.rcParams.update({
        "figure.facecolor": "#161b22",
        "axes.facecolor":   "#161b22",
        "axes.edgecolor":   "#30363d",
        "axes.labelcolor":  "#8b949e",
        "xtick.color":      "#8b949e",
        "ytick.color":      "#8b949e",
        "text.color":       "#e6edf3",
        "grid.color":       "#21262d",
        "grid.linewidth":   0.8,
    })
 
def plot_outcomes(pred):
    dark_style()
    fig, ax = plt.subplots(figsize=(7, 3.5))
    labels = [
        f"{pred['home_team']}\nWin",
        "Draw",
        f"{pred['away_team']}\nWin",
    ]
    probs  = [pred["home_win_prob"], pred["draw_prob"], pred["away_win_prob"]]
    colors = ["#3fb950", "#8b949e", "#f85149"]
    bars   = ax.barh(labels, probs, color=colors, height=0.5, edgecolor="none")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Probability (%)")
    ax.set_title("Match Outcome Probabilities", fontsize=13, fontweight="bold", color="#e6edf3")
    ax.axvline(33.3, color="#30363d", linestyle="--", linewidth=0.8)
    for bar, prob in zip(bars, probs):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                f"{prob}%", va="center", fontsize=11, fontweight="bold")
    ax.grid(axis="x", alpha=0.4)
    ax.spines[["top","right","bottom","left"]].set_visible(False)
    fig.tight_layout()
    return fig
 
def plot_scorers(pred):
    dark_style()
    fig, ax = plt.subplots(figsize=(5, 3))
    scorers = list(pred["top_scorer_probs"].keys())
    probs   = list(pred["top_scorer_probs"].values())
    colors  = ["#58a6ff", "#d29922"]
    ax.bar(scorers, probs, color=colors[:len(scorers)], width=0.4, edgecolor="none")
    ax.set_ylabel("Anytime Goal %")
    ax.set_title("Top Scorer Probabilities", fontsize=12, fontweight="bold", color="#e6edf3")
    ax.set_ylim(0, 100)
    for i, (sc, p) in enumerate(zip(scorers, probs)):
        ax.text(i, p + 1.5, f"{p}%", ha="center", fontsize=10, fontweight="bold")
    ax.spines[["top","right","left"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig
 
def plot_score_grid(pred):
    dark_style()
    scores = pred["top_scores"]
    labels = list(scores.keys())
    probs  = list(scores.values())
    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.bar(labels, probs, color="#58a6ff", edgecolor="#30363d", linewidth=0.6)
    ax.set_xlabel("Score (Home – Away)")
    ax.set_ylabel("Probability (%)")
    ax.set_title("Most Likely Scorelines", fontsize=12, fontweight="bold", color="#e6edf3")
    for bar, p in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"{p}%", ha="center", va="bottom", fontsize=9)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    return fig
 
# ── Form display ────────────────────────────────────────────────────────────────
 
def form_html(team: str) -> str:
    colour = {3: "#3fb950", 1: "#d29922", 0: "#f85149"}
    dots = "".join(
        f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;'
        f'background:{colour[r]};margin:2px;"></span>'
        for r in team_stats[team]["form"]
    )
    return dots
 
# ── Sidebar: league table simulator ────────────────────────────────────────────
 
def run_season_sim(n: int = 500) -> dict[str, dict]:
    teams = list(team_stats.keys())
    totals: dict[str, list] = {t: [] for t in teams}
    for _ in range(n):
        pts: dict[str, int]  = {t: 0 for t in teams}
        gd:  dict[str, int]  = {t: 0 for t in teams}
        for home, away in combinations(teams, 2):
            hxg, axg = expected_goals(home, away)
            hg = np.random.poisson(hxg)
            ag = np.random.poisson(axg)
            diff = hg - ag
            gd[home] += diff; gd[away] -= diff
            if hg > ag:  pts[home] += 3
            elif hg == ag: pts[home] += 1; pts[away] += 1
            else:          pts[away] += 3
            # Reverse fixture
            hxg2, axg2 = expected_goals(away, home)
            hg2 = np.random.poisson(hxg2)
            ag2 = np.random.poisson(axg2)
            diff2 = hg2 - ag2
            gd[away] += diff2; gd[home] -= diff2
            if hg2 > ag2:  pts[away] += 3
            elif hg2 == ag2: pts[away] += 1; pts[home] += 1
            else:           pts[home] += 3
        ranked = sorted(teams, key=lambda t: (pts[t], gd[t]), reverse=True)
        for pos, t in enumerate(ranked):
            totals[t].append(pos + 1)
    return {t: {"avg_pos": round(np.mean(v), 1), "title_pct": round(sum(1 for p in v if p == 1) / n * 100, 1),
                "top4_pct": round(sum(1 for p in v if p <= 4) / n * 100, 1),
                "rel_pct":  round(sum(1 for p in v if p >= 18) / n * 100, 1)}
            for t, v in totals.items()}
 
# ── Main UI ─────────────────────────────────────────────────────────────────────
 
st.markdown("<h1 style='text-align:center;font-size:3rem;letter-spacing:4px;'>⚽ EPL MATCH PREDICTOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8b949e;margin-top:-10px;margin-bottom:30px;'>Monte Carlo simulation · 10,000 iterations per match</p>", unsafe_allow_html=True)
 
tab1, tab2 = st.tabs(["🔮 Match Predictor", "📊 Season Simulator"])
 
# ─── Tab 1: Match Predictor ──────────────────────────────────────────────────
with tab1:
    teams_list = list(team_stats.keys())
    col_l, col_vs, col_r = st.columns([2, 0.7, 2])
 
    with col_l:
        home_team = st.selectbox("🏠 Home Team", teams_list, index=0, key="home")
    with col_vs:
        st.markdown("<div style='text-align:center;padding-top:28px;font-family:Bebas Neue,sans-serif;font-size:2rem;color:#8b949e;'>VS</div>", unsafe_allow_html=True)
    with col_r:
        away_options = [t for t in teams_list if t != home_team]
        away_team = st.selectbox("✈️ Away Team", away_options, index=1, key="away")
 
    # Form badges
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown(f"<div style='text-align:center'>Last 5: {form_html(home_team)}</div>", unsafe_allow_html=True)
    with fc2:
        st.markdown(f"<div style='text-align:center'>Last 5: {form_html(away_team)}</div>", unsafe_allow_html=True)
 
    st.write("")
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        predict = st.button("⚡ PREDICT MATCH")
 
    if predict:
        with st.spinner("Running simulation..."):
            pred = simulate_match(home_team, away_team)
 
        # ── VS header
        st.markdown(
            f"<div class='vs-header'>{home_team}  {pred['avg_home_goals']} – {pred['avg_away_goals']}  {away_team}</div>",
            unsafe_allow_html=True
        )
 
        # ── Outcome probability cards
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value green'>{pred['home_win_prob']}%</div>
                <div class='label'>🏠 {home_team} Win</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value gray'>{pred['draw_prob']}%</div>
                <div class='label'>🤝 Draw</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value red'>{pred['away_win_prob']}%</div>
                <div class='label'>✈️ {away_team} Win</div>
            </div>""", unsafe_allow_html=True)
 
        # ── Betting markets
        st.markdown("<div class='section-title'>📈 Betting Markets</div>", unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value gold'>{pred['btts']}%</div>
                <div class='label'>Both Teams Score</div>
            </div>""", unsafe_allow_html=True)
        with b2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value gold'>{pred['over_2_5']}%</div>
                <div class='label'>Over 2.5 Goals</div>
            </div>""", unsafe_allow_html=True)
        with b3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value' style='color:#58a6ff'>{pred['clean_home']}%</div>
                <div class='label'>{home_team} Clean Sheet</div>
            </div>""", unsafe_allow_html=True)
        with b4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value' style='color:#58a6ff'>{pred['clean_away']}%</div>
                <div class='label'>{away_team} Clean Sheet</div>
            </div>""", unsafe_allow_html=True)
 
        # ── Charts
        st.markdown("<div class='section-title'>📊 Charts</div>", unsafe_allow_html=True)
        ch1, ch2 = st.columns(2)
        with ch1:
            st.pyplot(plot_outcomes(pred))
        with ch2:
            st.pyplot(plot_score_grid(pred))
 
        # ── Top scorers
        if pred["top_scorer_probs"]:
            st.markdown("<div class='section-title'>🥅 Top Scorer Odds</div>", unsafe_allow_html=True)
            _, sc_col, _ = st.columns([1, 2, 1])
            with sc_col:
                st.pyplot(plot_scorers(pred))
 
        # ── xG breakdown
        st.markdown("<div class='section-title'>🔬 Expected Goals (xG)</div>", unsafe_allow_html=True)
        xg1, xg2 = st.columns(2)
        with xg1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value' style='color:#3fb950'>{pred['home_xg']}</div>
                <div class='label'>{home_team} xG</div>
            </div>""", unsafe_allow_html=True)
        with xg2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value' style='color:#f85149'>{pred['away_xg']}</div>
                <div class='label'>{away_team} xG</div>
            </div>""", unsafe_allow_html=True)
 
# ─── Tab 2: Season Simulator ─────────────────────────────────────────────────
with tab2:
    st.markdown("### 🏆 Season Finish Probabilities")
    st.markdown("<p style='color:#8b949e'>Simulates 500 full 38-game seasons using the Monte Carlo model.</p>", unsafe_allow_html=True)
 
    if st.button("🚀 Run Season Simulation (takes ~15s)"):
        with st.spinner("Simulating 500 seasons... ⏳"):
            results = run_season_sim(500)
 
        sorted_teams = sorted(results.keys(), key=lambda t: results[t]["avg_pos"])
 
        dark_style()
        fig, ax = plt.subplots(figsize=(10, 7))
        y_pos = range(len(sorted_teams))
        title_pcts = [results[t]["title_pct"] for t in sorted_teams]
        top4_pcts  = [results[t]["top4_pct"]  for t in sorted_teams]
        rel_pcts   = [results[t]["rel_pct"]   for t in sorted_teams]
 
        ax.barh(list(y_pos), top4_pcts,  color="#58a6ff", alpha=0.6, label="Top 4 %",    height=0.6)
        ax.barh(list(y_pos), title_pcts, color="#3fb950", alpha=0.9, label="Title %",    height=0.6)
        ax.barh(list(y_pos), [-r for r in rel_pcts], color="#f85149", alpha=0.7, label="Relegation %", height=0.6)
 
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(sorted_teams, fontsize=9)
        ax.axvline(0, color="#30363d", linewidth=0.8)
        ax.set_xlabel("Probability (%)")
        ax.set_title("Season Outcome Probabilities", fontsize=13, fontweight="bold", color="#e6edf3")
        ax.legend(loc="lower right", facecolor="#21262d", edgecolor="#30363d", labelcolor="#e6edf3")
        ax.spines[["top","right"]].set_visible(False)
        fig.tight_layout()
        st.pyplot(fig)
 
        # Table
        st.markdown("<div class='section-title'>📋 Full Season Table</div>", unsafe_allow_html=True)
        table_data = {
            "Team":        sorted_teams,
            "Avg Position": [results[t]["avg_pos"]  for t in sorted_teams],
            "Title %":     [results[t]["title_pct"] for t in sorted_teams],
            "Top 4 %":     [results[t]["top4_pct"]  for t in sorted_teams],
            "Relegation %":[results[t]["rel_pct"]   for t in sorted_teams],
        }
        import pandas as pd
        df = pd.DataFrame(table_data)
        df.index = range(1, len(df) + 1)
        st.dataframe(df, use_container_width=True)
 
    else:
        st.info("Click the button above to simulate a full season. This may take around 15 seconds.")
        
