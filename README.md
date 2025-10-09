# EPL Match Predictor
A Python Streamlit application that predicts English Premier League match outcomes using team stats, recent form, and Monte Carlo simulations. Users select home and away teams from dropdown menus, and the app predicts the likely score, win/draw/lose probabilities, and top scorer chances.

## Features
- Predict match outcomes based on team attack, defense, and recent form  
- Home advantage factored in  
- Monte Carlo simulations for probabilistic predictions  
- Top scorer probabilities  
- Interactive dropdowns with graphs for match probabilities and scorers  

## Installation
1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd EPLMatchPredictor
## Usage
Run the Streamlit application:
   ```bash
   streamlit run app.py
```
A browser window will open automatically. Select the home and away teams to view predictions.

## Dataset
Team stats (attack, defense, recent form, top scorer) are embedded in `app.py`. You can extend it with all EPL teams and updated stats.

## How It Works
1. Loads team stats (attack, defense, recent form, top scorer)  
2. Calculates a combined team strength score  
3. Applies home advantage  
4. Runs Monte Carlo simulations to estimate:
   - Average goals
   - Probability of home win, draw, away win
   - Likelihood of top scorers scoring

## Technologies
- Python
- Numpy
- Matplotlib
- Streamlit

## Notes
- Monte Carlo simulations generate probabilistic match predictions.  
- Top scorer probabilities are estimated from simulated goals.  
- Dropdown menus prevent selecting the same team as home and away.

