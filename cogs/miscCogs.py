from discord.ext import commands
from config import SHEET_URL

class Misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='credits')
    async def show_credits(self, ctx):
        await ctx.send(
            "Made by c00per and Hnff for the Tokyo Ghoul: Break the Chains (Global) server!"
        )

    @commands.command(name='sheet')
    async def show_sheet(self, ctx):
        await ctx.send(f"Here's my [sheet]({SHEET_URL})")

async def setup(bot):
    await bot.add_cog(Misc(bot))