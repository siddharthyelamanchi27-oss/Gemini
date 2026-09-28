import streamlit as st
import math
import random
import time
from streamlit_keyup import st_keyup

# ============================================================
# STARLIGHT GUARDIANS
# Streamlit version of the original game
# ============================================================

st.set_page_config(
    page_title="Starlight Guardians",
    page_icon="⭐",
    layout="wide"
)

# ------------------------------------------------------------
# Friendly names
# ------------------------------------------------------------

CLASS_CONFIG = {
    "STAR RANGER": {
        "weapon": "Comet Claws",
        "color": "#ff4f6d",
        "base_hp": 10,
        "base_speed": 3.4
    },
    "SKY MAGE": {
        "weapon": "Rainbow Cannon",
        "color": "#38d9ff",
        "base_hp": 8,
        "base_speed": 3.0
    },
    "ROBO HERO": {
        "weapon": "Spark Scythe",
        "color": "#50ff7a",
        "base_hp": 9,
        "base_speed": 3.2
    },
    "SHADOW SCOUT": {
        "weapon": "Moon Dagger",
        "color": "#ff55c8",
        "base_hp": 7,
        "base_speed": 4.0
    },
    "COSMIC EXPLORER": {
        "weapon": "Galaxy Blade",
        "color": "#b44cff",
        "base_hp": 8,
        "base_speed": 2.8
    }
}

ENEMY_CONFIG = {
    "STAR BUG": (1.8, 2.5, 3.0, 0.5, 1, 13, "#ff55aa"),
    "ROCKET BOT": (0.9, 1.4, 4.0, 0.6, 1, 15, "#ffe044"),
    "SHIELD BOT": (1.6, 2.2, 7.0, 1.0, 1, 16, "#389cff"),
    "MEGA BOT": (1.0, 1.4, 14.0, 1.8, 2, 24, "#ff4655")
}

UPGRADES = {
    "STAR RANGER": {
        "claw_reach": {"name": "Comet Reach", "lvl": 1, "max": 5,
                       "desc": "Wider attack range (+12 each level)"},
        "blood_siphon": {"name": "Star Energy", "lvl": 0, "max": 5,
                         "desc": "Chance to recover 1 HP after a hit (+5%)"},
        "frenzy_rate": {"name": "Meteor Rush", "lvl": 0, "max": 5,
                        "desc": "Chance to enter a speed boost"},
        "thick_hide": {"name": "Starlight Armor", "lvl": 0, "max": 5,
                       "desc": "Chance to block incoming damage (+8%)"},
        "apex_roar": {"name": "Hero Cheer", "lvl": 0, "max": 5,
                      "desc": "Defeating a Rocket Bot stuns nearby enemies"},
        "vitality_core": {"name": "Energy Core", "lvl": 0, "max": 5,
                          "desc": "Increases maximum HP (+2)"}
    },
    "SKY MAGE": {
        "divine_spark": {"name": "Rainbow Sparks", "lvl": 0, "max": 5,
                         "desc": "Attacks can jump between nearby enemies"},
        "time_dilation": {"name": "Cloud Time", "lvl": 0, "max": 5,
                          "desc": "Dash creates a short slow-motion effect"},
        "plague_ring": {"name": "Magic Aura", "lvl": 0, "max": 5,
                        "desc": "Nearby enemies take periodic damage"},
        "aegis_shield": {"name": "Bubble Shield", "lvl": 1, "max": 5,
                         "desc": "Shield returns faster"},
        "smite_strike": {"name": "Star Strike", "lvl": 0, "max": 5,
                         "desc": "Every 5th hit gets a bonus"},
        "divine_grace": {"name": "Cloud Step", "lvl": 0, "max": 5,
                         "desc": "Move faster during slow motion"}
    },
    "ROBO HERO": {
        "thruster_fuel": {"name": "Turbo Fuel", "lvl": 1, "max": 5,
                          "desc": "Dash cooldown is reduced"},
        "shock_field": {"name": "Spark Field", "lvl": 0, "max": 5,
                        "desc": "Periodically sends out a shockwave"},
        "shrapnel_burst": {"name": "Gear Burst", "lvl": 0, "max": 5,
                           "desc": "Picking up a star can create a small burst"},
        "overclock": {"name": "Turbo Swing", "lvl": 1, "max": 5,
                      "desc": "Attacks recharge faster"},
        "nanite_armor": {"name": "Helper Shield", "lvl": 0, "max": 5,
                         "desc": "Getting hit gives temporary protection"},
        "plasma_blade": {"name": "Spark Blade", "lvl": 0, "max": 5,
                         "desc": "Hits can cause extra damage over time"}
    },
    "SHADOW SCOUT": {
        "decoy_illusion": {"name": "Buddy Decoy", "lvl": 0, "max": 5,
                           "desc": "Dash leaves a friendly decoy"},
        "blink_strike": {"name": "Quick Swap", "lvl": 0, "max": 5,
                         "desc": "Swap with a nearby enemy and stun it"},
        "fatal_precision": {"name": "Perfect Aim", "lvl": 1, "max": 5,
                            "desc": "Critical hits become stronger"},
        "shadow_dash": {"name": "Moon Dash", "lvl": 1, "max": 5,
                        "desc": "Dash protection lasts longer"},
        "executioner": {"name": "Finishing Move", "lvl": 0, "max": 5,
                        "desc": "Very weak enemies can be finished quickly"},
        "spirit_drift": {"name": "Moon Speed", "lvl": 0, "max": 5,
                         "desc": "Increases movement speed"}
    },
    "COSMIC EXPLORER": {
        "event_horizon": {"name": "Gravity Buddy", "lvl": 0, "max": 5,
                          "desc": "Pulls nearby enemies closer"},
        "void_collapse": {"name": "Star Burst", "lvl": 0, "max": 5,
                          "desc": "Defeated enemies can damage nearby enemies"},
        "void_regen": {"name": "Cosmic Regen", "lvl": 0, "max": 5,
                       "desc": "Slowly restores health"},
        "singularity_power": {"name": "Galaxy Core", "lvl": 1, "max": 5,
                              "desc": "Increases attack power"},
        "rift_slip": {"name": "Galaxy Trail", "lvl": 0, "max": 5,
                      "desc": "Dash leaves a slowing zone"},
        "null_barrier": {"name": "Cosmic Barrier", "lvl": 0, "max": 5,
                         "desc": "Hits recharge your energy shield"}
    }
}


# ------------------------------------------------------------
# Session-state setup
# ------------------------------------------------------------

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
    st.session_state.particles = []
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
    st.session_state.rift_zones = []
    st.session_state.burn_enemies = []
    spawn_wave()


def add_message(message):
    st.session_state.messages.insert(0, message)
    st.session_state.messages = st.session_state.messages[:8]


def get_upgrade_level(upgrade_id):
    return UPGRADES[st.session_state.player_class].get(
        upgrade_id, {}
    ).get("lvl", 0)


def start_new_game():
    cls = st.session_state.player_class
    cfg = CLASS_CONFIG[cls]

    hp_boost = (
        get_upgrade_level("vitality_core") * 2
        if cls == "STAR RANGER" else 0
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
    st.session_state.particles = []
    st.session_state.rift_zones = []
    st.session_state.burn_enemies = []
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

        speed = random.uniform(cfg[0], cfg[1])

        if enemy_type == "STAR BUG":
            speed += st.session_state.wave * 0.08
        elif enemy_type == "MEGA BOT":
            speed += st.session_state.wave * 0.04
        else:
            speed += st.session_state.wave * 0.06

        hp = cfg[2] + st.session_state.wave * cfg[3]

        enemies.append({
            "x": x,
            "y": y,
            "type": enemy_type,
            "speed": speed,
            "hp": hp,
            "max_hp": hp,
            "damage": cfg[4],
            "size": cfg[5],
            "color": cfg[6],
            "stun": 0
        })

    st.session_state.enemies = enemies


def buy_upgrade(upgrade_id):
    upgrades = UPGRADES[st.session_state.player_class]
    upgrade = upgrades[upgrade_id]

    lvl = upgrade["lvl"]
    cost = 5 + lvl * 8

    if lvl >= upgrade["max"]:
        add_message("⭐ That upgrade is already maxed!")
        return

    if st.session_state.shards < cost:
        add_message("Not enough ⭐ stars yet!")
        return

    st.session_state.shards -= cost
    upgrade["lvl"] += 1
    add_message(f"✨ {upgrade['name']} upgraded to level {upgrade['lvl']}!")


# ------------------------------------------------------------
# Game mechanics
# ------------------------------------------------------------

def move_player(dx, dy):
    if st.session_state.state != "GAMEPLAY":
        return

    cls = st.session_state.player_class

    speed = CLASS_CONFIG[cls]["base_speed"]

    if cls == "STAR RANGER" and st.session_state.frenzy_timer > 0:
        speed *= 1.4

    if cls == "SHADOW SCOUT":
        speed *= 1 + get_upgrade_level("spirit_drift") * 0.08

    if cls == "SKY MAGE" and st.session_state.slow_timer > 0:
        if get_upgrade_level("divine_grace") > 0:
            speed *= 1.25

    if st.session_state.slow_timer > 0:
        speed *= 0.85

    st.session_state.player_x = max(
        5, min(95, st.session_state.player_x + dx * speed)
    )
    st.session_state.player_y = max(
        5, min(95, st.session_state.player_y + dy * speed)
    )

    update_enemies()


def update_enemies():
    slow_factor = 0.35 if st.session_state.slow_timer > 0 else 1.0

    for enemy in st.session_state.enemies:
        if enemy["stun"] > 0:
            enemy["stun"] -= 1
            continue

        dx = st.session_state.player_x - enemy["x"]
        dy = st.session_state.player_y - enemy["y"]
        dist = max(0.01, math.hypot(dx, dy))

        speed = enemy["speed"] * slow_factor

        enemy["x"] += dx / dist * speed
        enemy["y"] += dy / dist * speed

        # Gravity Buddy
        if st.session_state.player_class == "COSMIC EXPLORER":
            lvl = get_upgrade_level("event_horizon")
            if lvl > 0 and dist < 30:
                pull = lvl * 0.4
                enemy["x"] += dx / dist * pull
                enemy["y"] += dy / dist * pull

        # Enemy touches player
        if dist < 5 and st.session_state.invincible_timer <= 0:
            take_damage(enemy["damage"])
            enemy["x"] -= dx / dist * 3
            enemy["y"] -= dy / dist * 3

    if st.session_state.slow_timer > 0:
        st.session_state.slow_timer -= 1

    if st.session_state.frenzy_timer > 0:
        st.session_state.frenzy_timer -= 1

    if st.session_state.invincible_timer > 0:
        st.session_state.invincible_timer -= 1

    if st.session_state.dash_cooldown > 0:
        st.session_state.dash_cooldown -= 1

    # Cosmic Regen
    regen_lvl = get_upgrade_level("void_regen")
    if regen_lvl > 0 and st.session_state.player_hp < st.session_state.max_hp:
        st.session_state.regen_timer += 1
        if st.session_state.regen_timer >= max(5, 25 - regen_lvl * 3):
            st.session_state.regen_timer = 0
            st.session_state.player_hp = min(
                st.session_state.max_hp,
                st.session_state.player_hp + 1
            )
            add_message("💚 Cosmic Regen restored 1 HP!")

    # Magic Aura
    aura_lvl = get_upgrade_level("plague_ring")
    if st.session_state.player_class == "SKY MAGE" and aura_lvl > 0:
        for enemy in st.session_state.enemies:
            dist = math.hypot(
                enemy["x"] - st.session_state.player_x,
                enemy["y"] - st.session_state.player_y
            )
            if dist < aura_lvl * 8:
                enemy["hp"] -= aura_lvl * 0.5

    # Spark Field
    shock_lvl = get_upgrade_level("shock_field")
    if st.session_state.player_class == "ROBO HERO" and shock_lvl > 0:
        if random.random() < 0.08:
            radius = 12 + shock_lvl * 3
            for enemy in st.session_state.enemies:
                dist = math.hypot(
                    enemy["x"] - st.session_state.player_x,
                    enemy["y"] - st.session_state.player_y
                )
                if dist < radius:
                    enemy["hp"] -= shock_lvl * 1.5
            add_message("⚡ Spark Field activated!")

    cleanup_enemies()


def take_damage(amount):
    cls = st.session_state.player_class

    # Bubble shield
    if cls == "SKY MAGE" and st.session_state.has_shield:
        st.session_state.has_shield = False
        add_message("🫧 Bubble Shield protected you!")
        return

    # Starlight Armor
    block_chance = (
        get_upgrade_level("thick_hide") * 0.08
        if cls == "STAR RANGER" else 0
    )

    if random.random() < block_chance:
        add_message("🛡️ Starlight Armor blocked the hit!")
        return

    # Helper Shield
    nanite = get_upgrade_level("nanite_armor")
    if cls == "ROBO HERO" and nanite > 0:
        st.session_state.invincible_timer = nanite * 2

    st.session_state.player_hp -= amount
    st.session_state.invincible_timer = max(
        st.session_state.invincible_timer, 3
    )

    add_message(f"💥 You lost {amount} HP!")

    if st.session_state.player_hp <= 0:
        st.session_state.player_hp = 0
        st.session_state.state = "GAME_OVER"


def attack():
    if st.session_state.state != "GAMEPLAY":
        return

    if not st.session_state.enemies:
        return

    cls = st.session_state.player_class

    # Attack the closest enemy
    target = min(
        st.session_state.enemies,
        key=lambda e: math.hypot(
            e["x"] - st.session_state.player_x,
            e["y"] - st.session_state.player_y
        )
    )

    dist = math.hypot(
        target["x"] - st.session_state.player_x,
        target["y"] - st.session_state.player_y
    )

    attack_range = 14

    if cls == "STAR RANGER":
        attack_range += get_upgrade_level("claw_reach") * 1.2

    if dist > attack_range:
        add_message("🎯 Move closer to an enemy!")
        update_enemies()
        return

    damage = 2.0

    # Galaxy Core
    if cls == "COSMIC EXPLORER":
        damage *= 1 + get_upgrade_level("singularity_power") * 0.15

    # Perfect Aim
    critical = False
    crit_lvl = get_upgrade_level("fatal_precision")

    if cls == "SHADOW SCOUT" and random.random() < 0.25:
        critical = True
        damage *= 2.0 + crit_lvl * 0.4

    # Star Ranger Meteor Rush
    if cls == "STAR RANGER":
        frenzy_lvl = get_upgrade_level("frenzy_rate")
        if frenzy_lvl > 0 and random.random() < frenzy_lvl * 0.15:
            st.session_state.frenzy_timer = 3
            add_message("☄️ Meteor Rush activated!")

    # Rainbow Sparks
    if cls == "SKY MAGE":
        spark_lvl = get_upgrade_level("divine_spark")
        if spark_lvl > 0 and random.random() < 0.35:
            for other in st.session_state.enemies:
                if other is not target:
                    d = math.hypot(
                        other["x"] - target["x"],
                        other["y"] - target["y"]
                    )
                    if d < 18:
                        other["hp"] -= spark_lvl * 1.5
                        break

    # Spark Blade
    if cls == "ROBO HERO":
        plasma_lvl = get_upgrade_level("plasma_blade")
        if plasma_lvl > 0 and random.random() < 0.4:
            target["hp"] -= plasma_lvl * 0.5

    target["hp"] -= damage
    st.session_state.hit_counter += 1

    if critical:
        add_message(f"🌟 PERFECT HIT! {damage:.1f} damage")
    else:
        add_message(f"✨ Attack dealt {damage:.1f} damage")

    # Star Energy
    siphon = get_upgrade_level("blood_siphon")
    if cls == "STAR RANGER" and siphon > 0:
        if random.random() < siphon * 0.05:
            st.session_state.player_hp = min(
                st.session_state.max_hp,
                st.session_state.player_hp + 1
            )
            add_message("❤️ Star Energy restored 1 HP!")

    # Cloud Time
    if cls == "SKY MAGE" and get_upgrade_level("time_dilation") > 0:
        if random.random() < 0.15:
            st.session_state.slow_timer = (
                get_upgrade_level("time_dilation") * 2
            )

    # Cosmic Barrier
    if cls == "COSMIC EXPLORER":
        barrier = get_upgrade_level("null_barrier")
        if barrier > 0:
            st.session_state.shield_energy = min(
                100,
                st.session_state.shield_energy + damage * barrier * 2
            )

    cleanup_enemies()
    update_enemies()


def dash():
    if st.session_state.state != "GAMEPLAY":
        return

    if st.session_state.dash_cooldown > 0:
        add_message("💨 Dash is still recharging!")
        return

    st.session_state.dash_cooldown = max(
        2,
        8 - get_upgrade_level("thruster_fuel")
    )

    st.session_state.invincible_timer = max(
        st.session_state.invincible_timer,
        2 + get_upgrade_level("shadow_dash")
    )

    # Move toward the center of the board.
    dx = 50 - st.session_state.player_x
    dy = 50 - st.session_state.player_y
    dist = max(1, math.hypot(dx, dy))

    st.session_state.player_x = max(
        5, min(95, st.session_state.player_x + dx / dist * 12)
    )
    st.session_state.player_y = max(
        5, min(95, st.session_state.player_y + dy / dist * 12)
    )

    if st.session_state.player_class == "SKY MAGE":
        if get_upgrade_level("time_dilation") > 0:
            st.session_state.slow_timer = (
                get_upgrade_level("time_dilation") * 2
            )

    if st.session_state.player_class == "SHADOW SCOUT":
        if get_upgrade_level("blink_strike") > 0 and st.session_state.enemies:
            target = min(
                st.session_state.enemies,
                key=lambda e: math.hypot(
                    e["x"] - st.session_state.player_x,
                    e["y"] - st.session_state.player_y
                )
            )
            d = math.hypot(
                target["x"] - st.session_state.player_x,
                target["y"] - st.session_state.player_y
            )

            if d < 30:
                old_x, old_y = st.session_state.player_x, st.session_state.player_y
                st.session_state.player_x = target["x"]
                st.session_state.player_y = target["y"]
                target["x"] = old_x
                target["y"] = old_y
                target["hp"] -= get_upgrade_level("blink_strike") * 2
                target["stun"] = 2

    add_message("💨 Dash!")
    update_enemies()


def collect_star():
    if not st.session_state.collectible_shards:
        return

    st.session_state.shards += 1
    st.session_state.score += 10
    st.session_state.collectible_shards.pop(0)
    add_message("⭐ You collected a Star!")

    if (
        st.session_state.player_class == "ROBO HERO"
        and get_upgrade_level("shrapnel_burst") > 0
    ):
        add_message("⚡ Gear Burst activated!")

    update_enemies()


def cleanup_enemies():
    defeated = []

    for enemy in st.session_state.enemies:
        if enemy["hp"] <= 0:
            defeated.append(enemy)

    for enemy in defeated:
        if enemy not in st.session_state.enemies:
            continue

        st.session_state.enemies.remove(enemy)
        st.session_state.score += int(enemy["max_hp"] * 10)

        if random.random() < 0.75:
            st.session_state.collectible_shards.append({
                "x": enemy["x"],
                "y": enemy["y"]
            })

        # Hero Cheer
        if (
            st.session_state.player_class == "STAR RANGER"
            and enemy["type"] == "ROCKET BOT"
            and get_upgrade_level("apex_roar") > 0
        ):
            for other in st.session_state.enemies:
                d = math.hypot(
                    other["x"] - enemy["x"],
                    other["y"] - enemy["y"]
                )
                if d < 20:
                    other["stun"] = 2

        # Star Burst
        if (
            st.session_state.player_class == "COSMIC EXPLORER"
            and get_upgrade_level("void_collapse") > 0
        ):
            lvl = get_upgrade_level("void_collapse")
            for other in st.session_state.enemies:
                d = math.hypot(
                    other["x"] - enemy["x"],
                    other["y"] - enemy["y"]
                )
                if d < 15:
                    other["hp"] -= lvl * 2

        add_message(f"🎉 {enemy['type']} defeated!")

    if not st.session_state.enemies:
        st.session_state.wave += 1
        st.session_state.state = "SHOP"



# ------------------------------------------------------------
# Keyboard controls
# ------------------------------------------------------------

def keyboard_controls():
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] input {
            height: 1px;
            min-height: 1px;
            padding: 0;
            border: 0;
            opacity: 0;
            position: absolute;
            left: -9999px;
        }
        div[data-testid="stTextInput"] label {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    key = st_keyup(
        "Keyboard controls",
        key="game_keyboard",
        debounce=100
    )

    if not key:
        return

    key = str(key).lower()

    if key in ("arrowup", "w"):
        move_player(0, -1)
        st.rerun()

    elif key in ("arrowdown", "s"):
        move_player(0, 1)
        st.rerun()

    elif key in ("arrowleft", "a"):
        move_player(-1, 0)
        st.rerun()

    elif key in ("arrowright", "d"):
        move_player(1, 0)
        st.rerun()

    elif key in (" ", "space"):
        dash()
        st.rerun()

    elif key in ("enter",):
        attack()
        st.rerun()


# ------------------------------------------------------------
# UI
# ------------------------------------------------------------

def show_board():
    # HTML board that replaces the Pygame canvas.
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
            f'<div class="enemy" title="{enemy["type"]}" '
            f'style="left:{enemy["x"]}%;top:{enemy["y"]}%;'
            f'background:{enemy["color"]};">'
            f'🤖<span class="hp" style="width:{hp_ratio*100}%"></span>'
            f'</div>'
        )

    for star in st.session_state.collectible_shards:
        items.append(
            f'<div class="star" style="left:{star["x"]}%;'
            f'top:{star["y"]}%;font-size:22px;">⭐</div>'
        )

    board = "".join(items)

    st.markdown(
        f"""
        <style>
        .game-board {{
            position: relative;
            width: 100%;
            height: 520px;
            background:
                linear-gradient(rgba(255,255,255,.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,.04) 1px, transparent 1px),
                #080b18;
            background-size: 40px 40px;
            border: 2px solid #3b82f6;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(59,130,246,.2);
        }}
        .player {{
            position:absolute;
            transform:translate(-50%,-50%);
            width:42px;
            height:42px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            border:3px solid white;
            box-shadow:0 0 18px rgba(255,255,255,.7);
            font-size:22px;
        }}
        .enemy {{
            position:absolute;
            transform:translate(-50%,-50%);
            width:34px;
            height:34px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            border:2px solid white;
            font-size:17px;
        }}
        .hp {{
            position:absolute;
            left:0;
            bottom:-7px;
            height:4px;
            background:#55ff77;
            border-radius:5px;
        }}
        .star {{
            position:absolute;
            transform:translate(-50%,-50%);
            filter:drop-shadow(0 0 8px #ffe044);
        }}
        </style>
        <div class="game-board">{board}</div>
        """,
        unsafe_allow_html=True
    )


def show_hud():
    hp = st.session_state.player_hp
    max_hp = st.session_state.max_hp
    shield = int(st.session_state.shield_energy)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("❤️ HP", f"{hp}/{max_hp}")
    c2.metric("🛡️ Energy", f"{shield}%")
    c3.metric("⭐ Stars", st.session_state.shards)
    c4.metric("🌊 Wave", st.session_state.wave)


def show_controls():
    st.subheader("🎮 Controls")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("⬆️ Move Up", use_container_width=True):
            move_player(0, -1)

    with c2:
        if st.button("⚔️ ATTACK", use_container_width=True, type="primary"):
            attack()

    with c3:
        if st.button("⬇️ Move Down", use_container_width=True):
            move_player(0, 1)

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("⬅️ Move Left", use_container_width=True):
            move_player(-1, 0)

    with c2:
        if st.button("💨 DASH", use_container_width=True):
            dash()

    with c3:
        if st.button("➡️ Move Right", use_container_width=True):
            move_player(1, 0)

    if st.session_state.collectible_shards:
        if st.button(
            "⭐ Collect Nearby Star",
            use_container_width=True
        ):
            collect_star()


def show_shop():
    st.title("🛠️ Star Workshop")
    st.write(
        f"Wave {st.session_state.wave - 1} complete! "
        f"You have **{st.session_state.shards} ⭐ stars**."
    )

    upgrades = UPGRADES[st.session_state.player_class]

    for i, (upgrade_id, upgrade) in enumerate(upgrades.items()):
        lvl = upgrade["lvl"]
        cost = 5 + lvl * 8

        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 4, 1])

            with c1:
                st.markdown(f"### {upgrade['name']}")
                st.write(f"Level {lvl}/{upgrade['max']}")

            with c2:
                st.write(upgrade["desc"])

            with c3:
                if lvl >= upgrade["max"]:
                    st.success("MAX")
                else:
                    if st.button(
                        f"⭐ {cost}",
                        key=f"upgrade_{upgrade_id}",
                        use_container_width=True
                    ):
                        buy_upgrade(upgrade_id)
                        st.rerun()

    st.divider()

    if st.button(
        "🚀 Start Next Wave",
        type="primary",
        use_container_width=True
    ):
        spawn_wave()
        st.session_state.state = "GAMEPLAY"
        st.rerun()


def show_menu():
    st.title("⭐ STARLIGHT GUARDIANS")
    st.subheader("🌈 Five Cosmic Heroes")

    st.write(
        "Choose a hero, explore the arena, collect stars, "
        "upgrade your abilities, and protect the galaxy!"
    )

    names = list(CLASS_CONFIG.keys())

    selected = st.selectbox(
        "Choose your hero",
        names,
        index=st.session_state.class_selection
    )

    st.session_state.player_class = selected
    st.session_state.class_selection = names.index(selected)

    cfg = CLASS_CONFIG[selected]

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"## {selected}")
        st.write(f"**Special Tool:** {cfg['weapon']}")
        st.write(f"**Starting HP:** {cfg['base_hp']}")
        st.write(f"**Speed:** {cfg['base_speed']}")

    with c2:
        descriptions = {
            "STAR RANGER": "A brave hero with strong attacks and extra armor.",
            "SKY MAGE": "A magical hero with a protective bubble and special powers.",
            "ROBO HERO": "A helpful robot with sparks, shields, and turbo abilities.",
            "SHADOW SCOUT": "A quick explorer with strong critical hits and dashes.",
            "COSMIC EXPLORER": "A space adventurer who uses gravity and galaxy energy."
        }

        st.info(descriptions[selected])

    if st.button(
        "🚀 Start Adventure",
        type="primary",
        use_container_width=True
    ):
        st.session_state.state = "GAMEPLAY"
        start_new_game()
        st.rerun()


def show_game_over():
    st.title("🌟 Adventure Complete!")

    st.metric("🌊 Waves Survived", st.session_state.wave)
    st.metric("🏆 Total Score", st.session_state.score)

    st.write(
        "Great job! Your cosmic adventure is over. "
        "You can restart and try a different hero."
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button(
            "🔄 Play Again",
            type="primary",
            use_container_width=True
        ):
            st.session_state.state = "GAMEPLAY"
            start_new_game()
            st.rerun()

    with c2:
        if st.button(
            "🏠 Return to Hero Select",
            use_container_width=True
        ):
            st.session_state.state = "MENU"
            st.rerun()


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------

if "state" not in st.session_state:
    reset_game()

st.markdown(
    """
    <style>
    .stApp {
        background: #080b18;
    }
    h1, h2, h3 {
        letter-spacing: .5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state.state == "MENU":
    show_menu()

elif st.session_state.state == "GAMEPLAY":
    st.title("⭐ STARLIGHT GUARDIANS")

    show_hud()
    show_board()

    st.write("")

    st.info(
        "⌨️ **Keyboard:** Arrow Keys or WASD = Move  •  "
        "Space = Dash  •  Enter = Attack"
    )

    keyboard_controls()

    with st.expander("🖱️ Mouse/Touch Controls", expanded=False):
        show_controls()

    st.divider()

    st.subheader("📜 Adventure Log")

    for message in st.session_state.messages:
        st.write(message)

    if st.button("🏠 Return to Menu"):
        st.session_state.state = "MENU"
        st.rerun()

elif st.session_state.state == "SHOP":
    show_shop()

elif st.session_state.state == "GAME_OVER":
    show_game_over()
