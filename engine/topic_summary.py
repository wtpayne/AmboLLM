from engine.common import Message, TopicSummary
from dataclasses import asdict
from openai import AsyncOpenAI  # type: ignore
from dotenv import load_dotenv
from database import database

load_dotenv()  # take environment variables from .env.

# Gets API key from `OPENAI_API_KEY` environment variable.
client = AsyncOpenAI()

MODEL = "gpt-4-1106-preview"
TEMPERATURE = 1.0


async def get_topic_summary_prompt(topic) -> Message:
    # TODO: more prompt engineering
    return Message(
        role="system",
        content=f"You are a summarization engine tasked with synthesizing general opinions on the topic of {topic} from separate conversations with various users. Each message represents a different user's perspective. Summarize the overall sentiments and key points expressed by the group in a few sentences. Use brief and concise language in your summary.",
    )


async def topic_summary(topic_id: str) -> TopicSummary:
    prompt = await get_topic_summary_prompt(topic_id)
    topic_summaries = database.get_summaries_for_question(topic_id)
    if len(topic_summaries) == 0:
        return TopicSummary(topic_id=topic_id, summary="No summaries yet.")
    messages = [
        Message(role="user", content=summary["summary"]) for summary in topic_summaries
    ]
    augmented_messages = [prompt, *messages]
    print("Augmented messages:", augmented_messages, end="\n\n")
    response = await client.chat.completions.create(
        model=MODEL,
        messages=list(map(asdict, augmented_messages)),  # type: ignore
        temperature=TEMPERATURE,
    )
    return TopicSummary(
        topic_id=topic_id,
        summary=response.choices[0].message.content,  # type: ignore
    )
