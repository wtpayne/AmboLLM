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

import openai as engine


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

db_topic      = sqlitedict.SqliteDict('db.sqlite',
                                      tablename = 'topic',
                                      autocommit = True)
db_transcript = sqlitedict.SqliteDict('db.sqlite',
                                      tablename = 'transcript',
                                      autocommit = True)
db_summary    = sqlitedict.SqliteDict('db.sqlite',
                                      tablename = 'summary',
                                      autocommit = True)

db_topic['First DB topic']  = {'users': []}
db_topic['Second DB topic'] = {'users': []}
db_topic['Third DB topic']  = {'users': []}

# -----------------------------------------------------------------------------
def _load_debate_topics():
    """
    """
    return [item for item in db_topic]


# -----------------------------------------------------------------------------
@bot.event
async def on_ready():
    """
    """
    print(f'Logged in as {bot.user.name}')


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


# -----------------------------------------------------------------------------
@bot.command()
async def summary(ctx):
    """
    """
    # Create the dropdown
    select = TopicSelect(_load_debate_topics())

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

    select = TopicSelect(_load_debate_topics())

    # -------------------------------------------------------------------------
    async def join_callback(interaction):
        """
        """
        print(repr(select.values))

        await interaction.response.send_message("Joined the topic!",
                                            ephemeral=True)

    btn_join = discord.ui.Button(
                            label = 'Join',
                            style = discord.ButtonStyle.blurple)
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