import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import csv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

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

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        await message.channel.send("Command: ![character name] [attribute]\nExample: !arima wit")
    
    if message.content.startswith('!'):
        parts = message.content[1:].split(maxsplit=1)

        if len(parts) == 1 and parts[0].lower() == "command":
            await message.channel.send("Command: ![character name] [attribute]\nExample: !arima wit")
            return
        
        if len(parts) == 1 and parts[0].lower() == "sheet":
            await message.channel.send(f"Here's my [sheet]({url})")
            return
        
        if len(parts) == 1 and parts[0].lower() == "youtube":
            await message.channel.send(f"Here's my [Youtube channel]({youtube})")
            return
        
        if len(parts) == 2:
            name = parts[0].lower()
            attribute = parts[1].upper()

            matching = [char for char in characters if name in char['Character'].lower()
                        and char['Attribute'] == attribute]
            if matching:
                for char in matching:
                    embed = discord.Embed(
                        title=char['Character'],
                        description=char['Title'],
                        color=colour[char['Attribute']]
                    )
                    embed.add_field(name="Attribute", value=char['Attribute'])
                    embed.add_field(name="Faction", value=char['Faction'])
                    embed.add_field(name="Tactic", value=char['Tactic'])
                    embed.add_field(name="Base CP", value=char['Base CP'])
                    embed.add_field(name="3x Cell CP", value=char['3x Cell CP'])
                    embed.add_field(name="4x Cell CP", value=char['4x Cell CP'])
                    embed.add_field(name="Base ATK", value=char['ATK'])
                    embed.add_field(name="Base DEF", value=char['DEF'])
                    embed.add_field(name="Base HP", value=char['HP'])
                    embed.add_field(name="Release Date", value=char['Release Date'])
                    embed.add_field(name="Obtained", value=char['Obtained'])
                    embed.set_footer(text="All Cell CP include LR cells (if any) without any upgrades\n" \
                                          "Base CP is extrapolated from Strategic Arena")

                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("Character not found! Make sure you typed correctly "
                                           "or try '!command' for a guide.")
        else:
            await message.channel.send("Invalid command! Try '!command' for a guide.") 
   
bot.run(TOKEN)