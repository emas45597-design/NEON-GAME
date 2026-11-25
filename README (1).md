# NEON SPACE SURVIVOR

A premium dark-themed, browser-based arcade game built with Python and Streamlit.

## Features
- Neon dark interface
- Interactive 7×7 mission map
- Directional button controls
- Collectible energy orbs and asteroid hazards
- Score, shields, turn counter, and session best score
- Win, game-over, and restart states
- No API keys or external assets required

## Project files
- `app.py` — complete runnable Streamlit game
- `Neon_Space_Survivor.ipynb` — notebook explaining and demonstrating the game logic
- `requirements.txt` — Python dependency list

## Run locally
Requires Python 3.9+.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and launch:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## How to play
1. Press the arrow buttons to move one cell per turn.
2. Collect all five energy orbs (💠) to win.
3. Avoid asteroids (☄️); each collision costs one shield.
4. You start with three shields. Earn points by moving and collecting orbs.
5. Restart the mission to create a new random sector.

## Notes
The best score is held in Streamlit session state and is not saved permanently. The notebook is an educational companion for the game rules; the Streamlit app is the full interactive version.
