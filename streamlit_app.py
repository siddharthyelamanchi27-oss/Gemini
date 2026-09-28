import math
import random
import time
import streamlit as st
from st_keyup import st_keyup

# ============================================================
# STARLIGHT GUARDIANS (Real-Time Keyboard Controls)
# ============================================================

st.set_page_config(
    page_title="Starlight Guardians", page_icon="⭐", layout="wide"
)

CLASS_CONFIG = {
    "STAR RANGER": {
        "weapon": "Comet Claws",
        "color": "#ff4f6d",
        "base_hp": 10,
        "base_speed": 3.4,
    },
    "SKY MAGE": {
        "weapon": "Rainbow Cannon",
        "color": "#38d9ff",
        "base_hp": 8,
        "base_speed": 3.0,
    },
    "ROBO HERO": {
        "weapon": "Spark Scythe",
        "color": "#50ff7a",
        "base_hp": 9,
        "base_speed": 3.2,
    },
    "SHADOW SCOUT": {
        "weapon": "Moon Dagger",
        "color": "#ff55c8",
        "base_hp": 7,
        "base_speed": 4.0,
    },
    "COSMIC EXPLORER": {
        "weapon": "Galaxy Blade",
        "color": "#b44cff",
        "base_hp": 8,
        "base_speed": 2.8,
    },
}

ENEMY_CONFIG = {
    "STAR BUG": (1.8, 2.5, 3.0, 0.5, 1, 13, "#ff55aa"),
    "ROCKET BOT": (0.9, 1.4, 4.0, 0.6, 1, 15, "#ffe044"),
    "SHIELD BOT": (1.6, 2.2, 7.0, 1.0, 1, 16, "#389cff"),
    "MEGA BOT": (1.0, 1.4, 14.0, 1.8, 2, 24, "#ff4655"),
}

UPGRADES = {
    "STAR RANGER": {
        "claw_reach": {
            "name": "Comet Reach",
            "lvl": 1,
            "max": 5,
            "desc": "Wider attack range",
        },
        "blood_siphon": {
            "name": "Star Energy",
            "lvl": 0,
            "max": 5,
            "desc": "Chance to recover HP",
        },
        "frenzy_rate": {
            "name": "Meteor Rush",
            "lvl": 0,
            "max": 5,
            "desc": "Speed boost chance",
        },
        "thick_hide": {
            "name": "Starlight Armor",
            "lvl": 0,
            "max": 5,
            "desc": "Damage block chance",
        },
        "apex_roar": {
            "name": "Hero Cheer",
            "lvl": 0,
            "max": 5,
            "desc": "Stun nearby enemies on kill",
        },
        "vitality_core": {
            "name": "Energy Core",
            "lvl": 0,
            "max": 5,
            "desc": "Max HP up",
        },
    },
    "SKY MAGE": {
        "divine_spark": {
            "name": "Rainbow Sparks",
            "lvl": 0,
            "max": 5,
            "desc": "Attacks jump to targets",
        },
        "time_dilation": {
            "name": "Cloud Time",
            "lvl": 0,
            "max": 5,
            "desc": "Slow motion effect",
        },
        "plague_ring": {
            "name": "Magic Aura",
            "lvl": 0,
            "max": 5,
            "desc": "Periodic damage aura",
        },
        "aegis_shield": {
            "name": "Bubble Shield",
            "lvl": 1,
            "max": 5,
            "desc": "Faster shield return",
        },
        "smite_strike": {
            "name": "Star Strike",
            "lvl": 0,
            "max": 5,
            "desc": "Bonus damage hits",
        },
        "divine_grace": {
            "name": "Cloud Step",
            "lvl": 0,
            "max": 5,
            "desc": "Faster in slow-mo",
        },
    },
    "ROBO HERO": {
        "thruster_fuel": {
            "name": "Turbo Fuel",
            "lvl": 1,
            "max": 5,
            "desc": "Dash cooldown down",
        },
        "shock_field": {
            "name": "Spark Field",
            "lvl": 0,
            "max": 5,
            "desc": "Periodic shockwave",
        },
        "shrapnel_burst": {
            "name": "Gear Burst",
            "lvl": 0,
            "max": 5,
            "desc": "Star pickup burst",
        },
        "overclock": {
            "name": "Turbo Swing",
            "lvl": 1,
            "max": 5,
            "desc": "Faster recharge",
        },
        "nanite_armor": {
            "name": "Helper Shield",
            "lvl": 0,
            "max": 5,
            "desc": "Protection on hit",
        },
        "plasma_blade": {
            "name": "Spark Blade",
            "lvl": 0,
            "max": 5,
            "desc": "Damage over time",
        },
    },
    "SHADOW SCOUT": {
        "decoy_illusion": {
            "name": "Buddy Decoy",
            "lvl": 0,
            "max": 5,
            "desc": "Decoy on dash",
        },
        "blink_strike": {
            "name": "Quick Swap",
            "lvl": 0,
            "max": 5,
            "desc": "Swap and stun enemy",
        },
        "fatal_precision": {
            "name": "Perfect Aim",
            "lvl": 1,
            "max": 5,
            "desc": "Stronger crits",
        },
        "shadow_dash": {
            "name": "Moon Dash",
            "lvl": 1,
            "max": 5,
            "desc": "Longer dash protection",
        },
        "executioner": {
            "name": "Finishing Move",
            "lvl": 0,
            "max": 5,
            "desc": "Quickly finish weak foes",
        },
        "spirit_drift": {
            "name": "Moon Speed",
            "lvl": 0,
            "max": 5,
            "desc": "Speed boost",
        },
    },
    "COSMIC EXPLORER": {
        "event_horizon": {
            "name": "Gravity Buddy",
            "lvl": 0,
            "max": 5,
            "desc": "Pull enemies closer",
        },
        "void_collapse": {
            "name": "Star Burst",
            "lvl": 0,
            "max": 5,
            "desc": "Explosive defeat",
        },
        "void_regen": {
            "name": "Cosmic Regen",
            "lvl": 0,
            "max": 5,
            "desc": "Passive healing",
        },
        "singularity_power": {
            "name": "Galaxy Core",
            "lvl": 1,
            "max": 5,
            "desc": "Attack power up",
        },
        "rift_slip": {
            "name": "Galaxy Trail",
            "lvl": 0,
            "max": 5,
            "desc": "Slowing dash trail",
        },
        "null_barrier": {
            "name": "Cosmic Barrier",
            "lvl": 0,
            "max": 5,
            "desc": "Recharge energy shield",
        },
    },
}


def reset_game():
    st.session_state.state = "MENU"
    st.session_state.class_selection = 0
    st.session_state.player_class = "STAR RANGER"
    st.session_state.shards = 5
    st.session_state.score = 0
    st.session_state.wave = 1
    st.session_state.player_x = 50
    st.session_state.player_y = 50
    st.session_state.enemies = []
    st.session_state.collectible_shards = []
    st.session_state.messages = []
    st.session_state.player_hp = 10
    st.session_state.max_hp = 10
    st.session_state.has_shield = False
    st.session_state.shield_energy = 100
    st.session_state.hit_counter = 0
    st.session_state.frenzy_timer = 0
    st.session_state.slow_timer = 0
    st.session_state.invincible_timer = 0
    st.session_state.dash_cooldown = 0
    st.session_state.regen_timer = 0
    spawn_wave()


def add_message(message):
    st.session_state.messages.insert(0, message)
    st.session_state.messages = st.session_state.messages[:8]


def get_upgrade_level(upgrade_id):
    return (
        UPGRADES[st.session_state.player_class]
        .get(upgrade_id, {})
        .get("lvl", 0)
    )


def start_new_game():
    cls = st.session_state.player_class
    cfg = CLASS_CONFIG[cls]
    hp_boost = (
        get_upgrade_level("vitality_core") * 2 if cls == "STAR RANGER" else 0
    )

    st.session_state.max_hp = cfg["base_hp"] + hp_boost
    st.session_state.player_hp = st.session_state.max_hp
    st.session_state.player_x = 50
    st.session_state.player_y = 50
    st.session_state.has_shield = cls == "SKY MAGE"
    st.session_state.shield_energy = 100
    st.session_state.hit_counter = 0
    st.session_state.frenzy_timer = 0
    st.session_state.slow_timer = 0
    st.session_state.invincible_timer = 0
    st.session_state.dash_cooldown = 0
    st.session_state.regen_timer = 0
    st.session_state.collectible_shards = []
    spawn_wave()


def spawn_wave():
    enemies = []
    amount = 6 + st.session_state.wave * 2

    for _ in range(amount):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(5, 95), 0
        elif edge == "bottom":
            x, y = random.randint(5, 95), 100
        elif edge == "left":
            x, y = 0, random.randint(5, 95)
        else:
            x, y = 100, random.randint(5, 95)

        pool = ["STAR BUG"]
        if st.session_state.wave >= 2:
            pool.append("ROCKET BOT")
        if st.session_state.wave >= 3:
            pool.append("SHIELD BOT")
        if st.session_state.wave >= 5:
            pool.append("MEGA BOT")

        enemy_type = random.choice(pool)
        cfg = ENEMY_CONFIG[enemy_type]
        speed = random.uniform(cfg[0], cfg[1]) + st.session_state.wave * 0.06
        hp = cfg[2] + st.session_state.wave * cfg[3]

        enemies.append(
            {
                "x": x,
                "y": y,
                "type": enemy_type,
                "speed": speed,
                "hp": hp,
                "max_hp": hp,
                "damage": cfg[4],
                "size": cfg[5],
                "color": cfg[6],
                "stun": 0,
            }
        )

    st.session_state.enemies = enemies


def move_player(dx, dy):
    if st.session_state.state != "GAMEPLAY":
        return

    cls = st.session_state.player_class
    speed = CLASS_CONFIG[cls]["base_speed"]

    if cls == "STAR RANGER" and st.session_state.frenzy_timer > 0:
        speed *= 1.4

    st.session_state.player_x = max(
        5, min(95, st.session_state.player_x + dx * speed)
    )
    st.session_state.player_y = max(
        5, min(95, st.session_state.player_y + dy * speed)
    )
    update_enemies()


def update_enemies():
    for enemy in st.session_state.enemies:
        if enemy["stun"] > 0:
            enemy["stun"] -= 1
            continue

        dx = st.session_state.player_x - enemy["x"]
        dy = st.session_state.player_y - enemy["y"]
        dist = max(0.01, math.hypot(dx, dy))

        enemy["x"] += dx / dist * enemy["speed"]
        enemy["y"] += dy / dist * enemy["speed"]

        if dist < 5 and st.session_state.invincible_timer <= 0:
            take_damage(enemy["damage"])
            enemy["x"] -= dx / dist * 3
            enemy["y"] -= dy / dist * 3

    if st.session_state.invincible_timer > 0:
        st.session_state.invincible_timer -= 1
    if st.session_state.dash_cooldown > 0:
        st.session_state.dash_cooldown -= 1

    cleanup_enemies()


def take_damage(amount):
    st.session_state.player_hp -= amount
    st.session_state.invincible_timer = 3
    add_message(f"💥 You lost {amount} HP!")

    if st.session_state.player_hp <= 0:
        st.session_state.player_hp = 0
        st.session_state.state = "GAME_OVER"


def attack():
    if not st.session_state.enemies:
        return
    target = min(
        st.session_state.enemies,
        key=lambda e: math.hypot(
            e["x"] - st.session_state.player_x,
            e["y"] - st.session_state.player_y,
        ),
    )
    dist = math.hypot(
        target["x"] - st.session_state.player_x,
        target["y"] - st.session_state.player_y,
    )

    if dist > 18:
        add_message("🎯 Too far to attack!")
        return

    target["hp"] -= 2.0
    add_message("✨ Attack hit enemy!")
    cleanup_enemies()


def handle_key_input(key):
    if not key:
        return
    k = key.lower()
    if k in ["w", "arrowup"]:
        move_player(0, -2)
    elif k in ["s", "arrowdown"]:
        move_player(0, 2)
    elif k in ["a", "arrowleft"]:
        move_player(-2, 0)
    elif k in ["d", "arrowright"]:
        move_player(2, 0)
    elif k == " ":
        attack()


def cleanup_enemies():
    defeated = [e for e in st.session_state.enemies if e["hp"] <= 0]
    for enemy in defeated:
        st.session_state.enemies.remove(enemy)
        st.session_state.score += 10
        if random.random() < 0.75:
            st.session_state.collectible_shards.append(
                {"x": enemy["x"], "y": enemy["y"]}
            )
        add_message(f"🎉 {enemy['type']} defeated!")

    if not st.session_state.enemies:
        st.session_state.wave += 1
        st.session_state.state = "SHOP"


def show_board():
    items = []
    px = st.session_state.player_x
    py = st.session_state.player_y
    color = CLASS_CONFIG[st.session_state.player_class]["color"]

    items.append(
        f'<div class="player" style="left:{px}%;top:{py}%;'
        f'background:{color};">⭐</div>'
    )

    for enemy in st.session_state.enemies:
        hp_ratio = max(0, min(1, enemy["hp"] / enemy["max_hp"]))
        items.append(
            f'<div class="enemy" style="left:{enemy["x"]}%;top:{enemy["y"]}%;'
            f'background:{enemy["color"]};">🤖'
            f'<span class="hp" style="width:{hp_ratio*100}%"></span></div>'
        )

    for star in st.session_state.collectible_shards:
        items.append(
            f'<div class="star" style="left:{star["x"]}%;top:{star["y"]}%;">⭐</div>'
        )

    board = "".join(items)
    st.markdown(
        f"""
        <style>
        .game-board {{
            position: relative; width: 100%; height: 500px;
            background: #080b18; border: 2px solid #3b82f6;
            border-radius: 12px; overflow: hidden;
        }}
        .player {{
            position: absolute; transform: translate(-50%,-50%);
            width: 36px; height: 36px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            border: 2px solid white; font-size: 18px;
        }}
        .enemy {{
            position: absolute; transform: translate(-50%,-50%);
            width: 30px; height: 30px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            border: 2px solid white; font-size: 14px;
        }}
        .hp {{
            position: absolute; left: 0; bottom: -6px; height: 3px; background: #55ff77;
        }}
        .star {{
            position: absolute; transform: translate(-50%,-50%); font-size: 18px;
        }}
        </style>
        <div class="game-board">{board}</div>
        """,
        unsafe_allow_html=True,
    )


def show_hud():
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("❤️ HP", f"{st.session_state.player_hp}/{st.session_state.max_hp}")
    c2.metric("⭐ Stars", st.session_state.shards)
    c3.metric("🌊 Wave", st.session_state.wave)
    c4.metric("🏆 Score", st.session_state.score)


def show_shop():
    st.title("🛠️ Star Workshop")
    st.write(
        f"Wave {st.session_state.wave - 1} complete! "
        f"You have **{st.session_state.shards} stars**."
    )
    if st.button("🚀 Start Next Wave", type="primary"):
        spawn_wave()
        st.session_state.state = "GAMEPLAY"
        st.rerun()


def show_menu():
    st.title("⭐ STARLIGHT GUARDIANS")
    names = list(CLASS_CONFIG.keys())
    selected = st.selectbox("Choose your hero", names)
    st.session_state.player_class = selected

    if st.button("🚀 Start Adventure", type="primary"):
        st.session_state.state = "GAMEPLAY"
        start_new_game()
        st.rerun()


def show_game_over():
    st.title("🌟 Adventure Complete!")
    if st.button("🔄 Play Again"):
        reset_game()
        st.rerun()


if "state" not in st.session_state:
    reset_game()

if st.session_state.state == "MENU":
    show_menu()
elif st.session_state.state == "GAMEPLAY":
    st.title("⭐ STARLIGHT GUARDIANS")
    show_hud()
    show_board()

    # Real-time keyboard input box using st_keyup!
    key_input = st_keyup(
        "🎮 Keyboard Control (Type W, A, S, D, or Space to attack):",
        key="keyboard",
    )
    if key_input:
        handle_key_input(key_input)
        st.rerun()

    st.divider()
    for msg in st.session_state.messages:
        st.write(msg)

elif st.session_state.state == "SHOP":
    show_shop()
elif st.session_state.state == "GAME_OVER":
    show_game_over()
