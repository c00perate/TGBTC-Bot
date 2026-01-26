import discord
from typing import Dict, List
from config import *

def create_character_embed(char: Dict) -> discord.Embed:
    character_slug = char['Character'].lower().replace(' ', '')
    title_slug = char['Title'].lower().replace(' ', '').replace('/', '')
    thumbnail_url = f"https://raw.githubusercontent.com/c00perate/btc-images/main/characters/{character_slug}-{title_slug}.png"
    
    embed = discord.Embed(
        title=f"{char['Character']} [{char['Title']}]",
        description=f"**{char['Attribute']}** | **{char['Faction']}** | **{char['Tactic']}**",
        color=COLOUR[char['Attribute']]
    )
    embed.set_thumbnail(url=thumbnail_url)
    
    fields = [
        ("Combat Power", f"**Base:** {char['Base CP']} (#{char['Base CP_rank']})\n"
                         f"**3x Cell:** {char['3x Cell CP']} (#{char['3x Cell CP_rank']})\n"
                         f"**4x Cell:** {char['4x Cell CP']} (#{char['4x Cell CP_rank']})", False),

        ("Base Stats", f"**ATK:** {char['Base ATK']} (#{char['Base ATK_rank']})\n"
                       f"**DEF:** {char['Base DEF']} (#{char['Base DEF_rank']})\n"
                       f"**HP:** {char['Base HP']} (#{char['Base HP_rank']})", False),

        ("Details", f"**Release Date:** {char['Release Date']}\n"
                    f"**Obtained:** {char['Obtained']}", False),
    ]
    
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    
    embed.set_footer(text="All Cell CP include LR cells without upgrades\n"
                          "Data taken from Strategic Arena")
    
    return embed

def create_team_embed(faction: str, team: Dict, char_db) -> discord.Embed:

    display_name = FACTION_DISPLAY[faction]['name']
    team_members = []
    overall_cp3 = 0
    overall_cp4 = 0
    
    for i in range(1, 6):
        char_name = team.get(f"char{i}")
        char_attr = team.get(f"attr{i}")
        char_title = team.get(f"title{i}")
        
        if not char_name:
            continue
        
        char = char_db.find_character(char_name, char_attr, char_title)
        if char:
            team_members.append(f"- {char['Character']} [{char['Title']}]")
            overall_cp3 += char['3x Cell CP']
            overall_cp4 += char['4x Cell CP']
    
    embed = discord.Embed(
        title=f"{display_name} Team",
        description=f"\n".join(team_members),
        color=FACTION_DISPLAY[faction]['colour']
    )

    embed.add_field(name="Ultimate", value=team['ult'], inline=False)
    embed.add_field(name="Overall CP", value=f"**3x Cell:** {str(overall_cp3)}\n"
                                             f"**4x Cell:** {str(overall_cp4)}")
    embed.set_thumbnail(url=f"https://raw.githubusercontent.com/c00perate/btc-images/main/factions/{faction.lower()}.png")
    
    return embed

def create_ranking_embed(stat_name: str, top_chars: list, stat_key: str, start_num: int) -> discord.Embed:
    description = '\n'.join(
        f"{i}. {char['Character']} [{char['Title']}] - {char[stat_key]}"
        for i, char in enumerate(top_chars, start=start_num)
    )

    embed = discord.Embed(
        title=f"Characters Ranked by {stat_name}",
        description=description,
        color=discord.Color.light_gray()
    )
    
    embed.set_footer(
        text="All Cell CP include LR cells without upgrades\n"
             "Data taken from Strategic Arena"
    )
    
    return embed

def create_name_embed(matches: list) -> discord.Embed:
    description = '\n'.join(
        f"{i}. {char['Character']} [{char['Title']}] - {char['Attribute']}"
        for i, char in enumerate(matches, start=1)
    )

    embed = discord.Embed(
        title="List of all Mentioned Characters:",
        description=description,
        color=discord.Color.light_gray()
    )

    embed.set_footer(text="Use ![name] [attribute] to view specific character")

    return embed

def create_cells_list_embed(matches: List[Dict], start_index: int = 0) -> discord.Embed:
    description = '\n'.join(
        f"{start_index + i + 1}. {cell['Character']} [{cell['Title']}] - {cell['Attribute']} ({cell['Type']})"
        for i, cell in enumerate(matches)
    )
    
    embed = discord.Embed(
        title="List of Cells",
        description=description,
        color=discord.Color.light_gray()
    )
    
    embed.set_footer(text="Use !cell [name] [attribute] to view a specific cell")
    
    return embed

def create_cells_embed(cell: Dict) -> discord.Embed:
    character_slug = cell['Character'].lower().replace(' ', '')
    title_slug = cell['Title'].lower().replace(' ', '').replace('/', '')
    type_slug = cell['Type'].lower()
    thumbnail_url = f"https://raw.githubusercontent.com/c00perate/btc-images/main/lrcells/{character_slug}-{title_slug}-{type_slug}.png"
    effect = cell['Effect'] if cell['Effect'] else None
    
    embed = discord.Embed(
        title=f"{cell['Character']} [{cell['Title']}]\n{cell['Type']} Cell",
        description=f"**Base Stat: {cell['Base Stat']} {cell['Type']}**",
        color=COLOUR[cell['Attribute']]
    )
    embed.set_thumbnail(url=thumbnail_url)
    
    fields = [
        ("Cell Stats", f"+{cell['Stat 1']} \t+{cell['Stat 2']} \n+{cell['Stat 3']} \t+{cell['Stat 4']}", False),
        ("Cell Effect", f"{cell['Description']}", False),
    ]
    
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    if effect:
        embed.set_footer(text=effect)
    
    return embed