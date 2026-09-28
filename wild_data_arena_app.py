import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Laser Ninja Arcade", page_icon="⚡", layout="centered"
)

# Arcade Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f4068, #162447, #1b1b2f);
        color: white;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #e94560, #f08a5d);
        color: white;
        font-weight: 900;
        font-size: 1.2rem;
        border-radius: 12px;
        padding: 0.75rem;
        border: 2px solid #fff;
        box-shadow: 0px 4px 15px rgba(233, 69, 96, 0.5);
        transition: 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background: linear-gradient(45deg, #f08a5d, #e94560);
    }
    .arena-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #e94560;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.3);
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    "<h1 style='text-align: center; color: #f08a5d; text-shadow: 0 0 10px"
    " #f08a5d;'>⚡ LASER NINJA ARCADE ⚡</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align: center; color: #e94560;'>🔥 BATTLE THE"
    " CYBER-THREATS! 🔥</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Threat Database
threats = [
    {
        "name": "🤖 CYBER-ZOMBIE",
        "desc": "A mechanical monster is charging right at you!",
        "correct_move": "⚔️ Sword Slash",
        "image": "🦾",
    },
    {
        "name": "🔥 PLASMA DRAGON",
        "desc": "Spitting a wave of burning digital fire!",
        "correct_move": "🛡️ Energy Shield",
        "image": "🐉",
    },
    {
        "name": "☄️ METEOR SHOWER",
        "desc": "Raining burning space rocks from above!",
        "correct_move": "🏃‍♂️ Super Jump",
        "image": "🌋",
    },
    {
        "name": "👻 LASER GHOST",
        "desc": "Phasing through walls with a blinding energy beam!",
        "correct_move": "🛡️ Energy Shield",
        "image": "⚡",
    },
]

# Initialize Game State
if "score" not in st.session_state:
  st.session_state.score = 0
if "health" not in st.session_state:
  st.session_state.health = 3
if "streak" not in st.session_state:
  st.session_state.streak = 0
if "current_threat" not in st.session_state:
  st.session_state.current_threat = random.choice(threats)

threat = st.session_state.current_threat

# HUD Display
col1, col2, col3 = st.columns(3)
with col1:
  st.metric("🏆 SCORE", st.session_state.score)
with col2:
  st.metric("❤️ HEALTH", "💖" * st.session_state.health)
with col3:
  st.metric("🔥 STREAK", f"x{st.session_state.streak}")

st.markdown("---")

# Threat Arena Box
st.markdown(
    f"""
    <div class="arena-box">
        <h2>{threat['image']} {threat['name']}</h2>
        <p style="font-size: 1.2rem; color: #ffecd2;">{threat['desc']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown("### 🎮 CHOOSE YOUR COMBAT MOVE:")

# Action Buttons
moves = ["⚔️ Sword Slash", "🛡️ Energy Shield", "🏃‍♂️ Super Jump"]

col_a, col_b, col_c = st.columns(3)

player_choice = None
with col_a:
  if st.button(moves[0]):
    player_choice = moves[0]
with col_b:
  if st.button(moves[1]):
    player_choice = moves[1]
with col_c:
  if st.button(moves[2]):
    player_choice = moves[2]

# Handle Choice Logic
if player_choice:
  if player_choice == threat["correct_move"]:
    st.balloons()
    st.success("💥 PERFECT COUNTER! Enemy defeated!")
    st.session_state.score += 100
    st.session_state.streak += 1
  else:
    st.error(
        f"❌ BAD MOVE! The threat required a **{threat['correct_move']}**!"
    )
    st.session_state.health -= 1
    st.session_state.streak = 0

  # Check Game Over
  if st.session_state.health <= 0:
    st.error("💀 GAME OVER! Your health ran out!")
    if st.button("🔄 PLAY AGAIN"):
      st.session_state.score = 0
      st.session_state.health = 3
      st.session_state.streak = 0
      st.session_state.current_threat = random.choice(threats)
      st.rerun()
  else:
    # Next Threat
    st.session_state.current_threat = random.choice(threats)
    if st.button("⚡ NEXT ROUND"):
      st.rerun()

# Hard Reset Button
st.markdown("---")
if st.button("🔄 RESET GAME"):
  st.session_state.score = 0
  st.session_state.health = 3
  st.session_state.streak = 0
  st.session_state.current_threat = random.choice(threats)
  st.rerun()
