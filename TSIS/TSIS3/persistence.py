import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

SETTINGS_FILE = BASE_DIR / "settings.json"
LEADERBOARD_FILE = BASE_DIR / "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_leaderboard([])
        return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def add_score(name, score, distance, coins):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": distance,
        "coins": coins
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]

    save_leaderboard(leaderboard)