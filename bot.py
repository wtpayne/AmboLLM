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
from engine.common import Message
from engine.chat_completion import chat_completion
from engine.chat_summary import chat_summary
from engine.topic_summary import topic_summary

import engine
from database import database


dotenv.load_dotenv()  # take environment variables from .env.


intents                 = discord.Intents.default()
intents.guilds          = True
intents.dm_messages     = True
intents.dm_reactions    = True
intents.message_content = True
intents.messages        = True
intents.reactions       = True
intents.guild_messages  = True
bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)


# -----------------------------------------------------------------------------
def _get_default_topics():
    """
    Return default topics.

    """
    database.add_question(
        "What are your thoughts on charging for parking for the local library?"
    )
    database.add_question("Would you rather allocate funding to improve local library services or renovating the local park?")
    return [it["text"] for it in database.get_questions()]


# -----------------------------------------------------------------------------
@bot.event
async def on_ready():
    """
    On startup, when bot ready to respond.

    """
    print(f"LOGIN: {bot.user.name}")


# -----------------------------------------------------------------------------
@bot.event
async def on_message(message):
    """
    On message from user.

    """
    if message.author == bot.user:
        return

    if not isinstance(message.channel, discord.channel.DMChannel):
        await bot.process_commands(message)
        return

    if message.content == None or message.content == "" or message.content.startswith('!'):
        return
    
    author             = message.author
    user_conversations = database.get_user_conversations(str(author))
    convo_id           = user_conversations["conversation"]
    question_id        = database.get_conversation_question_id(convo_id)
    role = "user"
    content = message.content

    database.add_message(convo_id, role, content)

    if user_conversations != None:
        maybe_messages = database.get_messages(convo_id)
        if maybe_messages is None:
            raise Exception(f"No conversation with id {convo_id} found")

        messages = [Message(**message) for message in maybe_messages]

        response = await chat_completion(question_id, messages)
    
    if not response: 
        return 


    database.add_message(convo_id, response.role, response.content)
    message_length = len(response.content)

    for i in range(0, message_length, 2000):
        if i < len(response.content):
            await message.channel.send(response.content[i : min(message_length, i+2000)])

    await bot.process_commands(message)


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

        list_name = [it["text"] for it in database.get_questions()]
        if not list_name:
            list_name = _get_default_topics()

        super().__init__(
            *args,
            **kwargs,
            options=[discord.SelectOption(label=name) for name in list_name],
        )

    # ---------------------------------------------------------------------
    async def callback(self, interaction):
        """
        Defer as we want to wait for a button to be pressed.

        """
        await interaction.response.defer(ephemeral=True)


# -----------------------------------------------------------------------------
@bot.command()
async def join(ctx):
    """
    Join a deliberation.

    """

    select_topic = TopicSelectMenu()

    # -------------------------------------------------------------------------
    async def join_callback(interaction):
        """ """

        topic_id = select_topic.values[0]
        user     = interaction.user

        try:
            await user.send(f'Topic: {topic_id}')
            await interaction.response.send_message('Topic joined.',
                                                    ephemeral = True)
            database.delete_user(str(user))

            database.add_user(str(user))
            database.add_user_conversation(str(user), topic_id)
        except discord.errors.Forbidden:
            await interaction.response.send_message(
                "Unable to send DM. Please check privacy settings.",
                ephemeral = True
            )

    button_join = discord.ui.Button(label="Join", style=discord.ButtonStyle.green)
    button_join.callback = join_callback
    view = discord.ui.View()
    view.add_item(select_topic)
    view.add_item(button_join)
    await ctx.send("Select topic:", view=view)


# -----------------------------------------------------------------------------
@bot.command()
async def done(ctx):
    """
    Indicate that the user is finished.

    """

    response = "Thank you for taking part in the topic!"
    await ctx.send(response)

    user_id = ctx.message.author

    user_conversations = database.get_user_conversations(str(user_id))
    convo_id           = user_conversations["conversation"]
    question_id        = database.get_conversation_question_id(convo_id)

    summary_response = await chat_summary(convo_id)
    if summary_response is None:
        raise Exception(f"No conversation with id {convo_id} found")
    print("Summary of conversation:", summary_response, end="\n\n")
    database.add_convo_summary(summary_response.summary, question_id)

    topic_summary_response = await topic_summary(question_id)
    database.add_question_summary(topic_summary_response.summary, question_id)
    print("Summary of topic:", topic_summary_response, end="\n\n")

# -----------------------------------------------------------------------------
@bot.command()
async def summary(ctx):
    """
    """

    select_topic = TopicSelectMenu()

    # -------------------------------------------------------------------------
    async def summary_callback(interaction):
        """
        """

        topic_id = select_topic.values[0]
        summary  = database.get_summary_for_question(topic_id)
        if summary:
            summary = "Summary is: " + summary["summary"]
            await interaction.response.send_message(
                                    summary,
                                    ephemeral = True)
        else:
            await interaction.response.send_message(
                                    'No summary found for question.',
                                    ephemeral = True)

    button_summary = discord.ui.Button(label = 'Summary',
                                       style = discord.ButtonStyle.green)
    button_summary.callback = summary_callback
    view = discord.ui.View()
    view.add_item(select_topic)
    view.add_item(button_summary)
    await ctx.send("Select a summary:", view=view)


# -----------------------------------------------------------------------------
def _main(argv=None):
    """ """

    if argv is None:
        argv = sys.argv

    bot.run(os.environ["TOKEN_DISCORD_AMBOLLM"])


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(_main())
