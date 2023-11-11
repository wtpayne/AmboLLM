from typing import List

from common import Message
from dataclasses import asdict
from engine import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0

# TODO: prompt engineering


async def chat_completion(messages: List[Message]) -> Message:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[asdict(message) for message in messages],
        temperature=TEMPERATURE,
    )
    return Message(
        role=response.choices[0].message.role,
        content=response.choices[0].message.content,
    )
