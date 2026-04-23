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
    "STR": discord.Color.red(),
    "DST": discord.Color.light_embed()
}

SEARCH_QUERIES = {
    "hp": {
        "rank": "Base HP_rank",
        "value": "Base HP"
    },
    "atk": {
        "rank": "Base ATK_rank",
        "value": "Base ATK"
    },
    "def": {
        "rank": "Base DEF_rank",
        "value": "Base DEF"
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
    "anteiku": {
        "name": "Anteiku",
        "colour": discord.Color.blue()
    },
    "aogiri": {
        "name": "Aogiri",
        "colour": discord.Color.red()
    },
    "ccg": {
        "name": "CCG",
        "colour": discord.Color.green()
    },
    "noorg":{
        "name": "No Org",
        "colour": discord.Color.light_grey()
    }
}

SHEET_URL = "https://docs.google.com/spreadsheets/d/1xTd6d87NKzWBIdyTXbvqlRKioALJq9LgdFnvcutXztY/edit?usp=sharing"
ERROR_URL = "https://raw.githubusercontent.com/c00perate/btc-images/main/error.png"

INFO = "All Cell CP include LR cells without upgrades\nData taken from Strategic Arena"
SERVER = "https://discord.gg/BE5GaYk6wq"