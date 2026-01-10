import discord
from discord.ext import commands
import csv
from config import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name="Type !command for a guide!"))

characters = []
with open('characters.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['Base CP'] = int(row['Base CP'])
        row['3x Cell CP'] = int(row['3x Cell CP'])
        row['4x Cell CP'] = int(row['4x Cell CP'])
        row['ATK'] = int(row['ATK'])
        row['DEF'] = int(row['DEF'])
        row['HP'] = int(row['HP'])
        row['Nicknames'] = str(row.get('Nicknames', ''))
        characters.append(row)

char_index = {}
for char in characters:
    key = (char['Character'].lower(), char['Attribute'])
    char_index[key] = char

    if char['Nicknames']:
        nicknames = char['Nicknames'].lower()
        for nickname in nicknames:
            if nickname: 
                key = (nickname, char['Attribute'])
                char_index[key] = char

teams = []
with open('teams.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        teams.append(row)

def calculate_rankings():
    stats = ['Base CP', 'ATK', 'DEF', 'HP', '3x Cell CP', '4x Cell CP']

    for stat in stats:
        sorted_chars = sorted(characters, key=lambda x: x[stat], reverse=True)
        for i, char in enumerate(sorted_chars):
            char[f'{stat}_rank'] = i + 1

calculate_rankings()

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

@bot.event
async def on_message(message):
    if message.author.id in BLOCKED_USERS:
        return

    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        if message.author.id == 1164259640452857906:
            await message.channel.send("hi matti")
        await message.channel.send("Try '!command' for help!")
        
    if message.content.startswith('!'):
        parts = message.content[1:].split(maxsplit=1).lower()
        
        if len(parts) == 1:
            if parts[0] == "command":
                await message.channel.send(
                    "Commands:\n\n"
                    "![character name] [attribute]\n"
                    "Example: !arima wit\n\n"
                    "!team [faction]\n"
                    "Example: !team noorg\n\n"
                    "!rank [attribute (hp, def, atk, 3x, 4x, base)]\n"
                    "Example: !rank hp"
                    )
                return
            if parts[0].lower() == "credits":
                await message.channel.send("Made by c00per and Hnff for the Tokyo Ghoul: Break the Chains (Global) server!")
                return

            if parts[0].lower() == "sheet":
                await message.channel.send(f"Here's my [sheet]({SHEET_URL})")
                return
            
            if parts[0].lower() == "youtube":
                await message.channel.send(f"Here's my [Youtube channel]({YOUTUBE_URL})")
                return
        
        elif len(parts) == 2:
            if parts[0].lower() == "team":
                category = parts[1].lower()
                if category not in FACTION_DISPLAY:
                    await message.channel.send(f"Invalid Parameter! use !team with a valid query or !command for more help!")
                    return
                display_name = FACTION_DISPLAY[category]

                embed = discord.Embed(
                    title = f"{display_name} Teams", 
                    description=f"Current meta teams for {display_name} faction", 
                    color=discord.Color.random())
                
                for i in range(len(teams)):
                    if(teams[i]['faction'].lower() == category):
                        embed.add_field(name=teams[i]['title'], 
                                        value=
                                            f"- {teams[i]['char1']}\n"
                                            f"- {teams[i]['char2']}\n"
                                            f"- {teams[i]['char3']}\n"
                                            f"- {teams[i]['char4']}\n"
                                            f"- {teams[i]['backup']}")
                        embed.add_field(name="Ultimate", value=f"{teams[i]['ult']}", inline=True)
                        embed.add_field(name="Description", value=f"{teams[i]['description']}",inline=False)

                await message.channel.send(embed=embed)
                return


            if parts[0].lower() == "rank":
                category = parts[1].lower()

                if category not in SEARCH_QUERIES:
                    await message.channel.send(f"Invalid Parameter! use !rank with a valid query or !command for more help!")
                    return

                basestr = ""

                rank_key = SEARCH_QUERIES[category]["rank"]
                characters.sort(key=lambda c: int(c[rank_key]))

                for i in range(0, 10):
                    basestr += (
                        f"{i + 1}. {characters[i]['Character']} [{characters[i]['Title']}]"
                        f" - {characters[i][SEARCH_QUERIES[category]['value']]}\n"
                        )

                embed = discord.Embed(title=f"Top 10 Chars ranked by {SEARCH_QUERIES[category]['value']}", 
                                    description=basestr, 
                                    color=discord.Color.light_gray())
                
                embed.set_footer(text="All Cell CP include LR cells (if any) without any upgrades\n"
                                    "Base CP is extrapolated from Strategic Arena")

                await message.channel.send(embed=embed)
                return

            name = parts[0].lower()
            attribute = parts[1].upper()

            key = (name.lower(), attribute)
            char = char_index.get(key)
            
            if char:
                embed = discord.Embed(
                    title=char['Character'],
                    description=char['Title'],
                    color=COLOUR[char['Attribute']]
                )
                embed.set_thumbnail(url = ERROR_URL)
                embed.add_field(name="Attribute", value=char['Attribute'])
                embed.add_field(name="Faction", value=char['Faction'])
                embed.add_field(name="Tactic", value=char['Tactic'])
                embed.add_field(name=f"Base CP ", value=f"{char['Base CP']} (#{char['Base CP_rank']})")
                embed.add_field(name=f"3x Cell CP ", value=f"{char['3x Cell CP']} (#{char['3x Cell CP_rank']})")
                embed.add_field(name=f"4x Cell CP ", value=f"{char['4x Cell CP']} (#{char['4x Cell CP_rank']})")
                embed.add_field(name=f"Base ATK ", value=f"{char['ATK']} (#{char['ATK_rank']})")
                embed.add_field(name=f"Base DEF ", value=f"{char['DEF']} (#{char['DEF_rank']})")
                embed.add_field(name=f"Base HP ", value=f"{char['HP']} (#{char['HP_rank']})")
                embed.add_field(name=f"Release Date", value=char['Release Date'])
                embed.add_field(name="Obtained", value=char['Obtained'])
                embed.set_footer(text="All Cell CP include LR cells (if any) without any upgrades\n"
                                    "Base CP is extrapolated from Strategic Arena")
                await message.channel.send(embed=embed)

            else:
                await message.channel.send("Character not found! Make sure you typed correctly "
                                        "or try '!command' for a guide.")
        
        else:
            await message.channel.send("Invalid command! Try '!command' for a guide.") 
   
bot.run(TOKEN)