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
    # TODO: more prompt engineering
    topic = database.get_question(topic_id)
    topic_summaries = "\n".join(
        [
            summary["summary"]
            for summary in database.get_summaries_for_question(topic_id)
        ]
    )
    return Message(
        role="system",
        content=f"""You are a mediator guiding a focused discussion on the topic of {topic} among a group. Your role is to maintain a strictly on-topic conversation, ensuring participants understand the nuances. Utilize concise language and refer to summaries from previous discussions (provided as topic_summaries) to highlight diverse perspectives. Keep the dialogue focused and help the user gain insights from varying viewpoints. 
        topic_summaries{topic_summaries}""",
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
