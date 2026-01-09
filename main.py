import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import csv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
BLOCKED_USERS = [int(id) for id in os.getenv("BLOCKED_USERS", "").split(",") if id]


intents = discord.Intents.default()
intents.message_content = True
url = "https://docs.google.com/spreadsheets/d/1xTd6d87NKzWBIdyTXbvqlRKioALJq9LgdFnvcutXztY/edit?usp=sharing"
youtube = "https://www.youtube.com/@ThisGreenDino"

bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name="Type !command for a guide!"))

colour = {
    "WIT": discord.Color.purple(),
    "PSY": discord.Color.yellow(),
    "SPD": discord.Color.blue(),
    "SKL": discord.Color.green(),
    "STR": discord.Color.red()
}

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
        characters.append(row)

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
        await message.channel.send("Command: ![character name] [attribute]\nExample: !arima wit")
    
    if message.content.startswith('!'):
        parts = message.content[1:].split(maxsplit=1)

        if len(parts) == 1 and parts[0].lower() == "command":
            await message.channel.send("""Commands:\n
                                       ![character name] [attribute]\n
                                       Example: !arima wit\n\n
                                       !team [faction]\n
                                       Example: !team noorg\n\n
                                       !rank [attribute (hp, def, atk, 3x, 4x, base)]\n
                                       Example: !rank hp""")
            return
        
        if len(parts) == 1 and parts[0].lower() == "credits":
            await message.channel.send("Made by c00per and Hnff for the Tokyo Ghoul: Break the Chains (Global) server!")
            return

        if len(parts) == 1 and parts[0].lower() == "sheet":
            await message.channel.send(f"Here's my [sheet]({url})")
            return
        
        if len(parts) == 1 and parts[0].lower() == "youtube":
            await message.channel.send(f"Here's my [Youtube channel]({youtube})")
            return
        
        if len(parts) == 2 and parts[0].lower() == "team":
            category = parts[1]
            if category.lower() not in "noorganteikuccgaogiri":
                await message.channel.send(f"Invalid Parameter! use !team with a valid query or !command for more help!")
                return

            embed = discord.Embed(
                title = f"{category.capitalize()} Teams", 
                description=f"Current meta teams for {category.capitalize()} faction", 
                color=discord.Color.random())
            
            for i in range(len(teams)):
                if(teams[i]['faction'] == category.lower()):
                    embed.add_field(name=teams[i]['title'], 
                                    value=f""" - {teams[i]['char1']}
                                               - {teams[i]['char2']}
                                               - {teams[i]['char3']}
                                               - {teams[i]['char4']}
                                               - {teams[i]['backup']}""")
                    embed.add_field(name="Ultimate", value=f"{teams[i]['ult']}", inline=True)
                    embed.add_field(name="Description", value=f"{teams[i]['description']}",inline=False)

            await message.channel.send(embed=embed)
            return


        if len(parts) == 2 and parts[0].lower() == "rank":
            category = parts[1]
            searchqueries = {"hp":"HP_rank", "atk":"ATK_rank", "def":"DEF_rank", 
                             "3x":"3x Cell CP_rank", "4x":"4x Cell CP_rank", "base":"Base CP_rank"}

            if category.lower() not in searchqueries:
                await message.channel.send(f"Invalid Parameter! use !rank with a valid query or !command for more help!")
                return

            basestr = ""
            for i in range(0, 10):
                basestr += f"""{i + 1}. {characters[i]['Character']} [{characters[i]['Title']}] 
                            - {characters[i][searchqueries[category]]}\n"""

            embed = discord.Embed(title=f"Top 10 Chars ranked by {searchqueries[category]}", 
                                  description=basestr, 
                                  color=discord.Color.light_gray())
            
            embed.set_footer(text=""""All Cell CP include LR cells (if any) without any upgrades\n
                                      Base CP is extrapolated from Strategic Arena""")

            await message.channel.send(embed=embed)
            return

        if len(parts) == 2:
            name = parts[0].lower()
            attribute = parts[1].upper()

            matching = [char for char in characters 
                        if (name in char['Character'].lower() or name in char['Nicknames'].lower())
                        and char['Attribute'] == attribute]
            if matching:
                for char in matching:
                    noimage = False
                    if os.path.isfile(f"images\{char['Character']}{char['Title']}.jpg") == True:
                        file = discord.File(f"images\{char['Character']}{char['Title']}.jpg", 
                                            filename= f"{char['Character']}{char['Title']}.jpg")
                    else:
                        file = discord.File(f"images\error.png", filename= f"error.png")
                        noimage = True
                    embed = discord.Embed(
                        title=char['Character'],
                        description=char['Title'],
                        color=colour[char['Attribute']]
                    )
                    if noimage == False:
                        embed.set_thumbnail(url=f"attachment://{char['Character']}{char['Title']}.jpg")
                    else:
                        embed.set_thumbnail(url=f"attachment://error.png")
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
                    embed.set_footer(text="""All Cell CP include LR cells (if any) without any upgrades\n
                                             Base CP is extrapolated from Strategic Arena""")

                    await message.channel.send(embed=embed, file=file)
            else:
                await message.channel.send("""Character not found! Make sure you typed correctly
                                              or try '!command' for a guide.""")
        
        else:
            await message.channel.send("Invalid command! Try '!command' for a guide.") 
   
bot.run(TOKEN)