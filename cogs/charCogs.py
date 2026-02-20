from discord.ext import commands
from characters import CharacterDatabase 
from embeds import create_character_embed, create_name_embed
from buttons import Paginator

class Characters(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.db = CharacterDatabase()

    async def handle_character_search(self, ctx):
        content = ctx.message.content
        
        if not content.startswith('!'):
            return
        
        parts = content[1:].split(maxsplit=1)
        
        if len(parts) == 1:
            name = parts[0]
            matches = self.db.find_name(name)

            if not matches:
                await ctx.send("Character not found! Make sure you typed correctly "
                            "or try `!command` for help!")
                return
            elif len(matches) == 1:
                embed = create_character_embed(matches[0])
                await ctx.send(embed=embed)
            else:
                embed = create_name_embed(matches)
                await ctx.send(embed=embed)

        elif len(parts) == 2:
            name, attribute = parts
            matches = self.db.find_characters(name, attribute)
            
            if not matches:
                await ctx.send("Character not found! Make sure you typed correctly "
                            "or try `!command` for help!")
                return
            
            embed = create_character_embed(matches[0])

            if len(matches) == 1:
                await ctx.send(embed=embed)

            elif len(matches) < 11:
                view = Paginator(matches, embed_factory=create_character_embed, author_id=ctx.author.id)
                message = await ctx.send(f"Found {len(matches)} matches:\n", embed=embed, view=view)
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
                message = await ctx.send(embed=embed, view=view)
                view.message = message

        else:
            await ctx.send("Invalid command! Try `!command` for help!")
            return
        

async def setup(bot):
    await bot.add_cog(Characters(bot))