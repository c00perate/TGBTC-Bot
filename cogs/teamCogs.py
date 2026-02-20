from discord.ext import commands
from config import FACTION_DISPLAY
from teams import TeamDatabase
from characters import CharacterDatabase
from embeds import create_team_embed

class Teams(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.team = TeamDatabase()
        self.char = CharacterDatabase()
    
    @commands.command(name='team')
    async def show_team(self, ctx, faction: str):
        faction_lower = faction.lower()
        
        if faction_lower not in FACTION_DISPLAY:
            await ctx.send("Invalid faction! Try `!command` for help.")
            return
        
        teams = self.team.get_teams_by_faction(faction_lower)
        
        if not teams:
            await ctx.send(f"No teams found for {faction}")
            return
        
        for team in teams:
            embed = create_team_embed(faction_lower, team, self.char)
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Teams(bot))