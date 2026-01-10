import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
BLOCKED_USERS = [int(id) for id in os.getenv("BLOCKED_USERS", "").split(",") if id]

COLOUR = {
    "WIT": discord.Color.purple(),
    "PSY": discord.Color.yellow(),
    "SPD": discord.Color.blue(),
    "SKL": discord.Color.green(),
    "STR": discord.Color.red()
}

SEARCH_QUERIES = {
    "hp": {
        "rank": "HP_rank",
        "value": "HP"
    },
    "atk": {
        "rank": "ATK_rank",
        "value": "ATK"
    },
    "def": {
        "rank": "DEF_rank",
        "value": "DEF"
    },
    "3x": {
        "rank": "3x Cell CP_rank",
        "value": "3x Cell CP"
    },
    "4x": {
        "rank": "4x Cell CP_rank",
        "value": "4x Cell CP"
    },
    "base": {
        "rank": "Base CP_rank",
        "value": "Base CP"
    }
}

FACTION_DISPLAY = {
    "anteiku":"Anteiku",
    "aogiri":"Aogiri",
    "ccg":"CCG",
    "noorg":"NoOrg"
}

SHEET_URL = "https://docs.google.com/spreadsheets/d/1xTd6d87NKzWBIdyTXbvqlRKioALJq9LgdFnvcutXztY/edit?usp=sharing"
YOUTUBE_URL = "https://www.youtube.com/@ThisGreenDino"
ERROR_URL = "https://raw.githubusercontent.com/c00perate/btc-images/main/error.png"