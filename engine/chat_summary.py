from typing import Union

from engine.common import Message, ChatSummary
from dataclasses import asdict
from openai import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv
from database import database

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0


async def get_chat_summary_prompt() -> Message:
    # TODO: more prompt engineering
    return Message(
        role="system",
        content="You are a summarization engine. Summarize the users opinion on the topic in a few sentences. Use brief and concise language.",
    )


async def chat_summary(chat_id: str) -> Union[ChatSummary, None]:
    prompt = await get_chat_summary_prompt()
    conversation = database.get_conversation(chat_id)
    if conversation is None:
        return None
    messages = [Message(**messages) for messages in conversation["messages"]]
    augmented_messages = [prompt, *messages]
    print("Augmented messages:", augmented_messages, end="\n\n")
    response = await client.chat.completions.create(
        model=MODEL,
        messages=list(map(asdict, augmented_messages)),  # type: ignore
        temperature=TEMPERATURE,
    )
    return ChatSummary(
        chat_id=chat_id,
        summary=response.choices[0].message.content,  # type: ignore
    )
