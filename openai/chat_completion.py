from itertools import tee
from typing import List

from dataclasses import dataclass, asdict
from openai import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0


@dataclass
class Message:
    """A message in the conversation.

    Role is either "system" for the prompt, "user" for user responses, or "assistant" for the model's responses.
    """

    role: str
    content: str


async def chat_completions(messages: List[Message]) -> Message:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[asdict(message) for message in messages],
        temperature=TEMPERATURE,
    )
    return Message(
        role=response.choices[0].message.role,
        content=response.choices[0].message.content,
    )
