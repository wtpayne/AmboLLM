from typing import List

from common import Message, ChatSummary
from dataclasses import asdict
from openai import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0

# TODO: prompt engineering
# TODO: fetch chat messages from database
# TODO: store chat summary in database
# Question: are the chat messages stored per topic id or only per chat id?


async def chat_summary(
    chat_id: str, topic_id: str, messages: List[Message]
) -> ChatSummary:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[asdict(message) for message in messages]
        + [asdict(Message(role="user", content="Summarize this conversation."))],
        temperature=TEMPERATURE,
    )
    return ChatSummary(
        chat_id=chat_id,
        topic_id=topic_id,
        summary=response.choices[0].message.content,
    )
