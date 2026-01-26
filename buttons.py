import discord
from typing import Dict, List
from config import *
from discord.ui import View, Button
from embeds import create_character_embed

class Paginator(View):
    def __init__(self, items, embed_factory, timeout=180):
        super().__init__(timeout=timeout)
        self.items = items
        self.embed_factory = embed_factory
        self.current_index = 0
        self.message = None

        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = (self.current_index == 0)
        self.children[1].disabled = (self.current_index == len(self.items) - 1)

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_buttons()
            embed = self.embed_factory(self.items[self.current_index])
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.current_index < len(self.items) - 1:
            self.current_index += 1
            self.update_buttons()
            embed = self.embed_factory(self.items[self.current_index])
            await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            await self.message.edit(view=self)