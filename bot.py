#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

import discord
import discord.ext.commands
import discord.ui
import dotenv
import sqlitedict

import engine
import database


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


# =========================================================================
class TopicSelectMenu(discord.ui.Select):
    """
    Dropdown-style select menu for debate topics.

    """
    # ---------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        ctor.

        """
        list_name = [it['text'] for it in database.get_questions()]

        # Make sure we have some sample questions as a fallback.
        #
        if not list_name:
            database.add_question(
                'Should a Flurb be allowed to mellifulate with a Roxious Nurble?')
            database.add_question(
                'Where has all the rum gone?')
            list_name = [it['text'] for it in database.get_questions()]

        super().__init__(
            *args,
            **kwargs,
            options=[discord.SelectOption(label = name) for name in list_name])

    # ---------------------------------------------------------------------
    async def callback(self, interaction):
        """
        Defer as we want to wait for a button to be pressed.

        """
        await interaction.response.defer(ephemeral=True)


# -----------------------------------------------------------------------------
@bot.command()
async def summary(ctx):
    """
    """
    # Create the dropdown
    select = TopicSelectMenu()

    # Create the view and add the dropdown to it
    view = discord.ui.View()
    view.add_item(select)

    # Send a message with the dropdown
    await ctx.send("Select a summary:", view=view)


# -----------------------------------------------------------------------------
@bot.command()
async def topic(ctx):
    """
    """

    select = TopicSelectMenu()

    # -------------------------------------------------------------------------
    async def join_callback(interaction):
        """
        """

        user = interaction.user
        try:
            await user.send(f"You have joined the topic: {select.values[0]}")
            await interaction.response.send_message("A DM has been sent to you!", ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.response.send_message("I'm unable to send you a DM. Please check your privacy settings.", ephemeral=True)

        await interaction.response.send_message("Joined the topic!",
                                            ephemeral=True)

    btn_join = discord.ui.Button(
                            label = 'Join',
                            style = discord.ButtonStyle.green)
    btn_join.callback = join_callback


    # Create the view and add the dropdown to it
    view = discord.ui.View()
    view.add_item(select)
    view.add_item(btn_join)


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