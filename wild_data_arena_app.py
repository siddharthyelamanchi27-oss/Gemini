import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Wild Data Arena - Arcade", page_icon="🔥", layout="centered"
)

# Custom Arcade Styling & Animations
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        font-weight: 900;
        font-size: 1.2rem;
        border-radius: 12px;
        padding: 0.75rem;
        border: 2px solid #fff;
        box-shadow: 0px 4px 15px rgba(255, 75, 43, 0.4);
        transition: 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
    }
    .arcade-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f2fe;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    "<h1 style='text-align: center; color: #00f2fe; text-shadow: 0 0 10px"
    " #00f2fe;'>🕹️ WILD DATA ARENA 🕹️</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align: center; color: #ff0844;'>💥 BOSS BATTLE"
    " EDITION 💥</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Action Database: Extreme Stats & Bosses
bosses = [
    {
        "name": "🐨 THE KOALA SLEEP MONSTER",
        "category": "ANIMAL BOSS",
        "stat_name": "Daily Nap Time",
        "value": 22,
        "unit": "Hours",
        "taunt": "I sleep through entire seasons, human! Try to match my laziness!",
        "image": "💤",
    },
    {
        "name": "🐌 THE 14,000-TOOTH BEAST",
        "category": "MUTANT SLUG",
        "stat_name": "Teeth Count",
        "value": 14000,
        "unit": "Teeth",
        "desc": "Chewing everything in sight with a conveyor belt of doom!",
        "taunt": "You can't brush fast enough for this smile!",
        "image": "🦷",
    },
    {
        "name": "🐋 BLUE WHALE TITAN",
        "category": "OCEAN COLOSSUS",
        "stat_name": "Tongue Weight",
        "value": 7000,
        "unit": "Pounds",
        "desc": "My tongue alone weighs as much as a heavy truck!",
        "taunt": "I'm too heavy for your scoreboard!",
        "image": "🌊",
    },
    {
        "name": "🪐 SATURN THE SPACE FLOAT",
        "category": "PLANETARY ALIEN",
        "stat_name": "Bathtub Float Level",
        "value": 1,
        "unit": "Status (1=Yes)",
        "desc": "Made of gas—ready to float in a cosmic bathtub!",
        "taunt": "Catch me if you can, I'm floating away!",
        "image": "🛸",
    },
    {
        "name": "☁️ MEGA-CLOUD 9000",
        "category": "SKY TORNADO",
        "stat_name": "Cloud Weight",
        "value": 1100000,
        "unit": "Pounds",
        "desc": "Looks fluffy, but packs a million pounds of rain power!",
        "taunt": "I'm about to rain destruction on your score!",
        "image": "⚡",
    },
    {
        "name": "⏳ VENUS TIME-WARP",
        "category": "TIME MASTER",
        "stat_name": "Hours in a Day",
        "value": 5832,
        "unit": "Hours",
        "desc": "Spins so slow that a single day takes longer than a year!",
        "taunt": "Time means nothing to my slow-motion spin!",
        "image": "🌀",
    },
]

# Initialize Game State
if "score" not in st.session_state:
  st.session_state.score = 0
if "streak" not in st.session_state:
  st.session_state.streak = 0
if "round" not in st.session_state:
  st.session_state.round = 1
if "current_boss" not in st.session_state:
  st.session_state.current_boss = random.choice(bosses)

boss = st.session_state.current_boss

# HUD Display
col_hud1, col_hud2, col_hud3 = st.columns(3)
with col_hud1:
  st.metric("🏆 SCORE", st.session_state.score)
with col_hud2:
  st.metric("🔥 STREAK", f"x{st.session_state.streak}")
with col_hud3:
  st.metric("⚡ STAGE", st.session_state.round)

st.markdown("---")

# Boss Arena Box
st.markdown(
    f"""
    <div class="arcade-box">
        <h2>{boss['image']} {boss['name']}</h2>
        <p style="color: #00f2fe; font-weight: bold; font-size: 1.1rem;">CLASS: {boss['category']}</p>
        <p style="font-style: italic; color: #ffecd2;">"{boss['taunt']}"</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(f"### 🎯 MISSION: Guess the **{boss['stat_name']}** ({boss['unit']})!")

# Dynamic Slider
max_limit = int(boss["value"] * 2) if boss["value"] > 1 else 10
player_guess = st.slider(
    "POWER SLIDER:",
    min_value=0,
    max_value=max_limit,
    value=int(boss["value"] / 2),
    step=1,
)

# Attack Button
if st.button("💥 STRIKE WITH GUESS!"):
  target_val = boss["value"]
  difference = abs(player_guess - target_val)

  if player_guess == target_val:
    st.balloons()
    st.markdown(
        "<h2 style='text-align: center; color: #00ff00;'>⚡ CRITICAL HIT!"
        " BULLSEYE! ⚡</h2>",
        unsafe_allow_html=True,
    )
    st.session_state.score += 50
    st.session_state.streak += 1
  elif difference <= target_val * 0.15:
    st.markdown(
        "<h2 style='text-align: center; color: #00f2fe;'>🔥 SUPER EFFECTIVE!"
        " SO CLOSE! 🔥</h2>",
        unsafe_allow_html=True,
    )
    st.session_state.score += 25
    st.session_state.streak += 1
  else:
    st.markdown(
        "<h2 style='text-align: center; color: #ff4b2b;'>💥 BOSS COUNTERED!"
        " YOU MISSED! 💥</h2>",
        unsafe_allow_html=True,
    )
    st.session_state.streak = 0

  st.info(
      f"🛡️ **Boss Real Stat:** {target_val} {boss['unit']}! — {boss['desc']}"
  )

  # Next Stage setup
  st.session_state.round += 1
  st.session_state.current_boss = random.choice(bosses)

  if st.button("🚀 NEXT BOSS STAGE"):
    st.rerun()

# Reset Arcade Button
st.markdown("---")
if st.button("🔄 HARD RESET ARCADE"):
  st.session_state.score = 0
  st.session_state.streak = 0
  st.session_state.round = 1
  st.session_state.current_boss = random.choice(bosses)
  st.rerun()
