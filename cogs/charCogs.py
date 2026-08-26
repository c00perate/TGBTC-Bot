import discord
from discord.ext import commands
from discord.commands import Option
from src.characters import CharacterDatabase
from src.embeds import create_name_embed, create_character_embed
from src.buttons import Paginator
from src.config import TEST_GUILD

class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = CharacterDatabase()

    #, guild_ids=[TEST_GUILD]
    @discord.slash_command(name="find-char", description="returns all characters with matching name and attribute")
    async def handle_character_search(self, ctx, name:str, attr:Option(str, "Enter the attribute of the character", required = False, default = ' ')):
        content = name + " " + attr
        parts = content.split(maxsplit=1)
        
        if len(parts) == 1:
            name = parts[0]
            matches = self.db.find_name(name)

            if not matches:
                await ctx.respond("Character not found! Make sure you typed correctly "
                            "or try `/command` for help!", ephemeral=True)
                return
            elif len(matches) == 1:
                embed = create_character_embed(matches[0])
                await ctx.respond(embed=embed)
            else:
                embed = create_name_embed(matches)
                await ctx.respond(embed=embed)

        elif len(parts) == 2:
            name, attribute = parts
            matches = self.db.find_characters(name, attribute)
            
            if not matches:
                await ctx.respond("Character not found! Make sure you typed correctly "
                            "or try `/command` for help!", ephemeral=True)
                return
            
            embed = create_character_embed(matches[0])

            if len(matches) == 1:
                await ctx.respond(embed=embed)

            elif len(matches) < 11:
                view = Paginator(matches, embed_factory=create_character_embed, author_id=ctx.author.id)
                message = await ctx.respond(f"Found {len(matches)} matches:\n", embed=embed, view=view)
                view.message = message

            else:
                #try not preloading all the embeds
                count = 0
                pages = []
                while count < len(matches):
                    page_embed = create_name_embed(
                        matches[count:count+10], 
                        start_index=count
                    )
                    pages.append(page_embed)
                    count += 10
                
                view = Paginator(pages, lambda e: e, author_id=ctx.author.id)
                embed = pages[0]
                message = await ctx.respond(embed=embed, view=view)
                view.message = message

        else:
            await ctx.respond("Invalid command! Try `/command` for help!", ephemeral=True)
            return

def setup(bot):
    bot.add_cog(Characters(bot))