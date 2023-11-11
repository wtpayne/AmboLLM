from typing import List

from common import Message, TopicSummary
from dataclasses import asdict
from openai import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0

# TODO: prompt engineering
# TODO: fetch chat summaries from database
# TODO: store topic summary in database


async def topic_summary(topic_id: str, messages: List[Message]) -> TopicSummary:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[asdict(message) for message in messages]
        + [asdict(Message(role="user", content="Summarize this conversation."))],
        temperature=TEMPERATURE,
    )
    return TopicSummary(
        topic_id=topic_id,
        summary=response.choices[0].message.content,
    )
