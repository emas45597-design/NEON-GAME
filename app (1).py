import random
import streamlit as st

st.set_page_config(page_title="Neon Space Survivor", page_icon="🚀", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Inter:wght@400;600;700&display=swap');
.stApp{background:radial-gradient(circle at 15% 0%,#1a2a50,#090f1e 48%,#050812);color:#eff6ff}
.block-container{max-width:1150px;padding-top:2rem}
h1,h2,h3{font-family:Orbitron,sans-serif}
.hero{padding:1.7rem;border:1px solid #2b4569;border-radius:22px;background:linear-gradient(120deg,#182b4b,#0d172b);box-shadow:0 16px 45px #0006}
.kicker{color:#4de8f4;letter-spacing:.2em;font-size:.75rem;font-weight:700}
.hero h1{font-size:clamp(2rem,4vw,3.2rem);background:linear-gradient(90deg,#fff,#4de8f4,#c3a6ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p,.muted{color:#a9bad3}
.metric{padding:1rem 1.2rem;border:1px solid #2b4569;border-radius:15px;background:linear-gradient(145deg,#142440,#0d1729)}
.metric small{color:#9eb2ce;letter-spacing:.12em;text-transform:uppercase}
.metric strong{display:block;font: bold 1.8rem Orbitron;margin-top:.35rem}
.panel{padding:1.1rem;border:1px solid #2b4569;border-radius:18px;background:#0e192c}
.cell{height:67px;border:1px solid #263d5d;border-radius:11px;background:#0a1425;display:flex;align-items:center;justify-content:center;font-size:1.7rem}
div.stButton>button{border:1px solid #365879;border-radius:11px;background:linear-gradient(135deg,#254674,#126779);color:white;font-weight:700;min-height:2.8rem}
div.stButton>button:hover{border-color:#4de8f4;color:white;box-shadow:0 0 16px #4de8f433}
hr{border-color:#263d5d}
</style>
""", unsafe_allow_html=True)

N = 7
START = (3, 6)

def start_game():
    hazards = set()
    while len(hazards) < 7:
        p = (random.randrange(N), random.randrange(N))
        if p != START:
            hazards.add(p)
    orbs = set()
    while len(orbs) < 5:
        p = (random.randrange(N), random.randrange(N))
        if p not in hazards and p != START:
            orbs.add(p)
    st.session_state.update(player=START, hazards=hazards, orbs=orbs,
                            score=0, lives=3, turns=0, status="playing",
                            message="Mission started. Recover all energy orbs!")

def move(dr, dc):
    if st.session_state.status != "playing":
        return
    r, c = st.session_state.player
    pos = (r + dr, c + dc)
    if not (0 <= pos[0] < N and 0 <= pos[1] < N):
        st.session_state.message = "Shield boundary detected. Choose another direction."
        return
    st.session_state.player = pos
    st.session_state.turns += 1
    st.session_state.score += 2
    if pos in st.session_state.hazards:
        st.session_state.hazards.remove(pos)
        st.session_state.lives -= 1
        st.session_state.message = "Asteroid collision! One shield lost."
    elif pos in st.session_state.orbs:
        st.session_state.orbs.remove(pos)
        st.session_state.score += 25
        st.session_state.message = "Energy orb recovered: +25 points!"
    else:
        st.session_state.message = "Safe flight. Keep going!"
    if st.session_state.turns % 4 == 0:
        st.session_state.score += 5
    if st.session_state.lives <= 0:
        st.session_state.status = "lost"
        st.session_state.message = "Ship destroyed. Mission failed."
    elif not st.session_state.orbs:
        st.session_state.status = "won"
        st.session_state.message = "Sector cleared! All energy orbs recovered."
    st.session_state.best = max(st.session_state.best, st.session_state.score)

if "status" not in st.session_state:
    st.session_state.best = 0
    start_game()

st.markdown("""<div class="hero"><div class="kicker">ARCADE MISSION • SECTOR 07</div>
<h1>NEON SPACE SURVIVOR</h1><p>Pilot through a hostile sector, recover every energy orb, dodge asteroid fields, and protect your shields.</p></div>""", unsafe_allow_html=True)
st.write("")
stats = st.columns(4)
values = [("SCORE", f"{st.session_state.score:03d}"),
          ("SHIELDS", "❤️ " * st.session_state.lives if st.session_state.lives else "0"),
          ("ORB TARGETS", str(len(st.session_state.orbs))),
          ("BEST SCORE", str(st.session_state.best))]
for col, (label, value) in zip(stats, values):
    col.markdown(f'<div class="metric"><small>{label}</small><strong>{value}</strong></div>', unsafe_allow_html=True)

st.write("")
board, controls = st.columns([1.55, 1], gap="large")
with board:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Mission map")
    st.caption("🚀 Your ship   ☄️ Asteroid   💠 Energy orb   · Empty space")
    for r in range(N):
        cells = st.columns(N, gap="small")
        for c in range(N):
            p = (r, c)
            icon = "🚀" if p == st.session_state.player else "☄️" if p in st.session_state.hazards else "💠" if p in st.session_state.orbs else "·"
            with cells[c]:
                st.markdown(f'<div class="cell">{icon}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with controls:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Flight controls")
    st.caption("Move one cell per turn.")
    disabled = st.session_state.status != "playing"
    _, mid, _ = st.columns(3)
    if mid.button("⬆️", use_container_width=True, disabled=disabled):
        move(-1, 0); st.rerun()
    left, mid, right = st.columns(3)
    if left.button("⬅️", use_container_width=True, disabled=disabled):
        move(0, -1); st.rerun()
    if mid.button("⬇️", use_container_width=True, disabled=disabled):
        move(1, 0); st.rerun()
    if right.button("➡️", use_container_width=True, disabled=disabled):
        move(0, 1); st.rerun()
    st.divider()
    st.markdown("**Mission status**")
    if st.session_state.status == "playing":
        st.info(st.session_state.message)
    elif st.session_state.status == "won":
        st.success(st.session_state.message); st.balloons()
    else:
        st.error(st.session_state.message)
    st.metric("Turns survived", st.session_state.turns)
    if st.button("🔄 Restart mission", use_container_width=True):
        start_game(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("How to play"):
    st.markdown("1. Use the arrow buttons to move around the 7×7 sector.\\n2. Collect all five 💠 energy orbs to win.\\n3. Avoid ☄️ asteroids; each collision costs one of your three shields.\\n4. Empty moves award points; orbs award bonus points.\\n5. Restart to generate a new random sector.")
st.caption("NEON SPACE SURVIVOR · Python + Streamlit · Best score lasts for this browser session.")
