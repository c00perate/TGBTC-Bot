import discord
from discord.ext import commands
from config import TOKEN
import os

intents = discord.Intents.default()

bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Connected to {len(bot.guilds)} servers")
    print(f"loaded cogs: {[cog for cog in bot.cogs]}")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"failed to start bot: {e}")


