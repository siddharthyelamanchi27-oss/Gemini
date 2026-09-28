import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Sci-Fi Arcade Arena", page_icon="⚡", layout="centered"
)

# Custom Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d0f18, #1a1c29, #25283d);
        color: white;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: #0d0f18;
        font-weight: 900;
        font-size: 1.1rem;
        border-radius: 10px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: #000;
    }
    .arcade-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f2fe;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    "<h1 style='text-align: center; color: #00f2fe;'>⚡ SCI-FI ARCADE"
    " ARENA ⚡</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='text-align: center; color: #ff0844;'>SELECT YOUR CLASS &"
    " UPGRADE YOUR GEAR</h4>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Initialize Session State
if "selected_class" not in st.session_state:
  st.session_state.selected_class = "TITAN"
if "energy_cells" not in st.session_state:
  st.session_state.energy_cells = 50
if "score" not in st.session_state:
  st.session_state.score = 0

# Class Definitions & Upgrades
classes_data = {
    "TITAN": {
        "icon": "🦾",
        "desc": "Heavy melee powerhouse with high energy defense.",
        "upgrades": {
            "Power Swipe": {
                "lvl": 1,
                "max": 5,
                "cost": 5,
                "desc": "Wider swipe range",
            },
            "Vitality Drain": {
                "lvl": 0,
                "max": 5,
                "cost": 8,
                "desc": "Chance to restore energy on hit",
            },
            "Turbo Surge": {
                "lvl": 0,
                "max": 5,
                "cost": 10,
                "desc": "Attack rate boost",
            },
            "Armor Plating": {
                "lvl": 0,
                "max": 5,
                "cost": 12,
                "desc": "Damage reduction shield",
            },
        },
    },
    "NEXUS": {
        "icon": "⚡",
        "desc": "Master of energy chains and time manipulation.",
        "upgrades": {
            "Plasma Chain": {
                "lvl": 0,
                "max": 5,
                "cost": 6,
                "desc": "Chain energy links",
            },
            "Chrono Warp": {
                "lvl": 0,
                "max": 5,
                "cost": 10,
                "desc": "Slow-motion duration boost",
            },
            "Static Field": {
                "lvl": 0,
                "max": 5,
                "cost": 8,
                "desc": "Tick-damage aura",
            },
            "Barrier Core": {
                "lvl": 1,
                "max": 5,
                "cost": 5,
                "desc": "Faster shield recharge",
            },
        },
    },
    "MECH": {
        "icon": "🤖",
        "desc": "Cybernetic specialist loaded with thrusters and EMPs.",
        "upgrades": {
            "Jet Boost": {
                "lvl": 1,
                "max": 5,
                "cost": 5,
                "desc": "Faster dash cooldown",
            },
            "EMP Burst": {
                "lvl": 0,
                "max": 5,
                "cost": 10,
                "desc": "Static explosion wave",
            },
            "Fragment Blast": {
                "lvl": 0,
                "max": 5,
                "cost": 8,
                "desc": "Releases energy shards",
            },
            "Turbo Drive": {
                "lvl": 1,
                "max": 5,
                "cost": 7,
                "desc": "Weapon swing frequency boost",
            },
        },
    },
}

# Sidebar Class Selection
st.sidebar.header("🕹️ ARCADE CONTROL")
chosen_class = st.sidebar.selectbox(
    "Choose Contender Class:", list(classes_data.keys())
)
st.session_state.selected_class = chosen_class

current_data = classes_data[chosen_class]

# HUD Display
col1, col2 = st.columns(2)
with col1:
  st.metric("🔋 ENERGY CELLS", st.session_state.energy_cells)
with col2:
  st.metric("🏆 ARCADE SCORE", st.session_state.score)

st.markdown("---")

# Display Class Card
st.markdown(
    f"""
    <div class="arcade-card">
        <h2>{current_data['icon']} CLASS: {chosen_class}</h2>
        <p style="color: #4facfe;">{current_data['desc']}</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown("### ⚙️ UPGRADE BAY")

# Upgrades Store Interface
for upg_name, details in current_data["upgrades"].items():
  cols = st.columns([3, 1, 1])
  with cols[0]:
    st.write(
        f"**{upg_name}** (Lvl {details['lvl']}/{details['max']}) —"
        f" *{details['desc']}*"
    )
  with cols[1]:
    cost = details["cost"] + (details["lvl"] * 5)
    st.write(f"💎 {cost} Cells")
  with cols[2]:
    if details["lvl"] < details["max"]:
      if st.button("UPGRADE", key=f"btn_{chosen_class}_{upg_name}"):
        if st.session_state.energy_cells >= cost:
          st.session_state.energy_cells -= cost
          details["lvl"] += 1
          st.success("Upgraded!")
          st.rerun()
        else:
          st.error("Not enough cells!")
    else:
      st.markdown("✅ **MAX**")

st.markdown("---")

# Action Simulation Button
# Action Simulation Button
if st.button("🚀 LAUNCH SIMULATION ARENA RUN"):
  earned = random.randint(15, 35)
  st.session_state.energy_cells += earned
  st.session_state.score += 100
  st.balloons()
  # Store the last earned amount in session state to display it persistently
  st.session_state.last_earned = earned
  st.success(
      f"🎉 Simulation complete! You collected **{earned} Energy Cells** and 100"
      " Score points!"
  )

# Display last reward if available
if "last_earned" in st.session_state:
  st.info(
      f"⚡ Last Mission Reward: +{st.session_state.last_earned} Energy Cells!"
  )
