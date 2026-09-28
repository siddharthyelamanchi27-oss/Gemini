import random
import streamlit as st

st.set_page_config(
    page_title="Wild Data Arena", page_icon="⚡", layout="centered"
)

st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.75rem;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .main {
        background-color: #f8fafc;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ WILD DATA ARENA! ⚡")
st.markdown(
    "### *Battle with real-world facts! Choose your power and conquer the"
    " arena!*"
)

fighters = [
    {
        "name": "🐨 The Super-Sleeper Koala",
        "category": "Animal",
        "stat_name": "Hours Slept Per Day",
        "value": 20,
        "unit": "hours",
        "desc": (
            "Spends most of its life in dreamland, waking up only to snack on"
            " leaves!"
        ),
    },
    {
        "name": "🐌 The Tooth-Machine Snail",
        "category": "Animal",
        "stat_name": "Number of Teeth",
        "value": 14000,
        "unit": "teeth",
        "desc": (
            "Has a tongue covered in thousands of microscopic teeth like a"
            " conveyor belt!"
        ),
    },
    {
        "name": "🐋 The Mega-Blue Whale",
        "category": "Animal",
        "stat_name": "Tongue Weight",
        "value": 7000,
        "unit": "pounds",
        "desc": "Its tongue alone weighs as much as an entire adult elephant!",
    },
    {
        "name": "🪐 The Floating Saturn",
        "category": "Space",
        "stat_name": "Density vs Water Scale",
        "value": 1,
        "unit": "Bathtub Float Status (1=Yes)",
        "desc": (
            "Made mostly of gas, meaning it would float if you had a big"
            " enough bathtub!"
        ),
    },
    {
        "name": "☁️ The Heavy Cloud",
        "category": "Weather",
        "stat_name": "Weight of 1 Fluffy Cloud",
        "value": 1100000,
        "unit": "pounds",
        "desc": (
            "Looks light as a feather, but it's packed with millions of"
            " gallons of water drops!"
        ),
    },
    {
        "name": "⏳ Time-Bending Venus",
        "category": "Space",
        "stat_name": "Hours in a Planet Day",
        "value": 5832,
        "unit": "hours",
        "desc": (
            "Spins so slowly that its day is actually longer than its whole"
            " year!"
        ),
    },
]

if "score" not in st.session_state:
  st.session_state.score = 0
if "round" not in st.session_state:
  st.session_state.round = 1
if "current_fighter" not in st.session_state:
  st.session_state.current_fighter = random.choice(fighters)
  st.session_state.secret_target = st.session_state.current_fighter["value"]

fighter = st.session_state.current_fighter

st.markdown(f"### 🔥 Round {st.session_state.round} | Score: 🏆 {st.session_state.score}")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
  st.markdown(f"**Contender:** {fighter['name']}")
  st.markdown(f"**Category:** {fighter['category']}")
with col2:
  st.markdown(f"**Special Stat:** {fighter['stat_name']}")

st.info(f"💡 **Mission Briefing:** {fighter['desc']}")

st.markdown(f"#### Can you guess the exact **{fighter['stat_name']}** ({fighter['unit']})?")

max_val = int(fighter["value"] * 2) if fighter["value"] > 1 else 10
user_guess = st.slider(
    "Slide to lock in your power level:",
    min_value=0,
    max_value=max_val,
    value=int(fighter["value"] / 2),
    step=1,
)

if st.button("🚀 LAUNCH GUESS!"):
  target = st.session_state.secret_target
  difference = abs(user_guess - target)

  if user_guess == target:
    st.balloons()
    st.success(
        f"🎯 BULLSEYE! Absolute perfection! The exact value was"
        f" **{target} {fighter['unit']}**!"
    )
    st.session_state.score += 10
  elif difference <= max(1, target * 0.2):
    st.success(
        f"🔥 SO CLOSE, HERO! You were right on the edge. The actual stat was"
        f" **{target} {fighter['unit']}**!"
    )
    st.session_state.score += 5
  else:
    st.warning(
        f"💥 BOOM! Wild guess, but the real data was **{target}"
        f" {fighter['unit']}**!"
    )

  st.session_state.round += 1
  st.session_state.current_fighter = random.choice(fighters)
  st.session_state.secret_target = st.session_state.current_fighter["value"]

  if st.button("⚡ NEXT BATTLE"):
    st.rerun()

if st.button("🔄 Reset Arena"):
  st.session_state.score = 0
  st.session_state.round = 1
  st.session_state.current_fighter = random.choice(fighters)
  st.session_state.secret_target = st.session_state.current_fighter["value"]
  st.rerun()