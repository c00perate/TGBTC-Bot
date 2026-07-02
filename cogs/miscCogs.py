import discord
from discord.ext import commands
from config import SHEET_URL

class Misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='credit', aliases=['credits'])
    async def show_credits(self, ctx):
        await ctx.send(
            "Made by c00per and Hnff for the Tokyo Ghoul: Break the Chains (Global) server!"
        )

    @commands.command(name='sheet')
    async def show_sheet(self, ctx):
        await ctx.send(f"Here's my [sheet]({SHEET_URL})")

    @commands.command(name='role')
    async def give_role(self, ctx, member: discord.Member, role: str):

        if not any(role.name == "Mod" for role in ctx.author.roles):
            return

        role = discord.utils.find(
            lambda r: r.name.lower() == role.lower(),
            ctx.guild.roles
        )
        
        if not role:
            await ctx.send("Role not found.")
            return

        try:
            await member.add_roles(role)
            await ctx.send(f"{member.mention} is now a {role.name}!")

        except Exception as e:
            await ctx.send("Couldn't assign role.")
            print(e)

    @commands.command(name='removerole')
    async def remove_role(self, ctx, member: discord.Member, role: str):

        #remove the and later this is just for tests
        if not any(role.name == "Mod" for role in ctx.author.roles) or ctx.author.id not in  [715421855716212777,482343889567744021,710221160754708630]:
            await ctx.send("boii u really though :joy: :joy: :v:")
            return

        role = discord.utils.find(
            lambda r: r.name.lower() == role.lower(),
            ctx.guild.roles
        )

        if not role:
            await ctx.send("Role not found.")
            return

        try:
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} is no longer a {role.name}!")

        except Exception as e:
            await ctx.send("Couldn't remove role.")
            print(e)

async def setup(bot):
    await bot.add_cog(Misc(bot))