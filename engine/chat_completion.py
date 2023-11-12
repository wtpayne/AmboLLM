from typing import List

from engine.common import Message
from dataclasses import asdict
from openai import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv
from database import database

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0


async def get_chat_completion_prompt(topic_id: str) -> Message:
    # TODO: prompt engineering
    topic_summaries = database.get_summaries_for_question(topic_id)
    return Message(
        role="system",
        content="You are a helpful assistant.",
    )


async def chat_completion(topic_id: str, messages: List[Message]) -> Message:
    prompt = await get_chat_completion_prompt(topic_id)
    augmented_messages = [prompt, *messages]
    print("Augmented messages:", augmented_messages, end="\n\n")
    response = await client.chat.completions.create(
        model=MODEL,
        messages=list(map(asdict, augmented_messages)),  # type: ignore
        temperature=TEMPERATURE,
    )
    return Message(
        role=response.choices[0].message.role,
        content=response.choices[0].message.content,  # type: ignore
    )
