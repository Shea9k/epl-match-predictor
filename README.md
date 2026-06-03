# EPL Match Predictor

> A Monte Carlo simulation engine for Premier League match outcomes — built with Python and Streamlit.
---

## What It Does

Select any two Premier League teams and the app runs **10,000 Monte Carlo simulations** to generate probabilistic predictions for the match. Rather than a single guess, you get a full probability distribution across every possible outcome.

**Match Predictor tab:**
- Win / Draw / Loss probabilities
- Expected goals (xG) for each team
- Both Teams to Score %
- Over 2.5 Goals %
- Clean sheet probabilities
- Most likely exact scorelines
- Top scorer anytime goal probabilities

**Season Simulator tab:**
- Simulates 500 full 38-game seasons
- Title win %, Top 4 %, and Relegation % for all 20 teams
- Full league table sorted by average finishing position

---

## How the Model Works

### Team Strength
Each team has three underlying stats:
- **Attack** — offensive quality (rated out of 100)
- **Defense** — defensive solidity (rated out of 100)
- **Form** — last 5 results (W=3, D=1, L=0), averaged

### Expected Goals (xG)
Rather than a single strength score, the model calculates xG by pitting each team's attack directly against the opponent's defence:

```
home_xG = BASE_GOALS × (home_attack / 80) × (80 / away_defense) × HOME_ADV × form_factor
away_xG = BASE_GOALS × (away_attack / 80) × (80 / home_defense)              × form_factor
```

- `BASE_GOALS = 1.35` (EPL average goals per team per game)
- `HOME_ADV = 1.12` (home advantage factor)
- Form adjusts xG by ±6% based on recent results

### Simulation
Goals for each simulation are drawn from a **Poisson distribution** parameterised by xG — which is the standard statistical model for football scoring. With 10,000 iterations, the resulting win/draw/loss probabilities are stable to within ~1%.

---

## Installation

**Requirements:** Python 3.8+

```bash
# 1. Clone the repo
git clone https://github.com/Shea9k/epl-match-predictor.git
cd epl-match-predictor

# 2. Install dependencies
pip install streamlit numpy matplotlib pandas

# 3. Run the app
streamlit run app.py
```

A browser window will open at `http://localhost:8501`.

---

## Screenshots

| Match Predictor | Season Simulator |
|---|---|
| Select two teams, hit Predict, get full breakdown | Simulate 500 seasons to see title & relegation odds |

---

## Teams Included

All 20 2024/25 Premier League teams with stats approximated from current season performance:

| Tier | Teams |
|---|---|
| Title contenders | Manchester City, Liverpool, Arsenal |
| Top 6 | Chelsea, Aston Villa, Tottenham |
| Established mid-table | Newcastle, Brighton, Fulham, Brentford, Nottm Forest |
| Lower mid-table | West Ham, Wolves, Crystal Palace, Bournemouth |
| Relegation zone | Everton, Leicester, Ipswich, Southampton |

---

## Tech Stack

| Library | Use |
|---|---|
| `streamlit` | Web UI and interactive components |
| `numpy` | Monte Carlo simulation engine |
| `matplotlib` | Charts and visualisations |
| `pandas` | Season simulator table display |

---

## Limitations & Notes

- Team stats are manually set approximations based on the 2024/25 season — they are not pulled from a live data source
- The model uses a simplified two-factor xG formula; it does not account for injuries, suspensions, tactical matchups, or head-to-head history
- Top scorer probabilities are estimated from simulated goals with a fixed 38% attribution rate — treat these as rough indicators only
- The season simulator runs ~20,000 matches per simulation run and takes ~15 seconds

---

## Potential Improvements

- [ ] Pull live team stats from a football data API (e.g. football-data.org)
- [ ] Add head-to-head record as a model factor
- [ ] Per-player goal probability model instead of top scorer only
- [ ] Historical accuracy backtesting
- [ ] Odds comparison vs bookmaker lines

---

