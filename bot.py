#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

import discord
import discord.ext.commands
import discord.ui
import dotenv


dotenv.load_dotenv()  # take environment variables from .env.


intents                 = discord.Intents.default()
intents.guilds          = True
intents.dm_messages     = True
intents.dm_reactions    = True
intents.message_content = True
intents.messages        = True
intents.reactions       = True
intents.guild_messages  = True
bot                     = discord.ext.commands.Bot(
                                        command_prefix = '!',
                                        intents        = intents)


# -----------------------------------------------------------------------------
@bot.event
async def on_ready():
    """
    """
    print(f'Logged in as {bot.user.name}')


# -----------------------------------------------------------------------------
@bot.command()
async def list(ctx):

    topics = ['First topic', 'Second topic']

    # =========================================================================
    class TopicSelect(discord.ui.Select):
        """
        """

        # ---------------------------------------------------------------------
        def __init__(self, topics, *args, **kwargs):
            """
            """
            options = [discord.SelectOption(label=topic) for topic in topics]
            super().__init__(*args, **kwargs, options=options)

        # ---------------------------------------------------------------------
        async def callback(self, interaction):
            """
            """
            await interaction.response.send_message(
                                    f"You selected {self.values[0]}",
                                    ephemeral=True)

    # Create the dropdown
    select = TopicSelect(topics)

    # Create the view and add the dropdown to it
    view = discord.ui.View()
    view.add_item(select)

    # Send a message with the dropdown
    await ctx.send("Select a topic:", view=view)


# -----------------------------------------------------------------------------
def _main(argv = None):
    """
    """

    if argv is None:
        argv = sys.argv

    bot.run(os.environ['TOKEN_DISCORD_AMBOLLM'])


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(_main())