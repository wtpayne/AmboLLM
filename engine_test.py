import asyncio
from engine.common import Message
from engine.chat_completion import chat_completion
from engine.chat_summary import chat_summary
from engine.topic_summary import topic_summary
from database import database
from typing import Tuple


def mock_database() -> Tuple[str, str, str]:
    user_id = "test_user_id"
    database.add_user(user_id)
    topic_id = database.add_question("What is the meaning of life?")
    chat_id = database.add_user_conversation(user_id, topic_id)

    database.add_message(
        chat_id,
        "system",
        "You are a helpful assistant here to ask the user about the meaning of life.",
    )
    database.add_message(chat_id, "user", "Hello, what are we here to speak about?")
    database.add_message(
        chat_id,
        "assistant",
        "We are here to speak about the meaning of life. What do you think the meaning of life is?",
    )
    database.add_message(chat_id, "user", "42.")
    return user_id, chat_id, topic_id


async def main():
    _, chat_id, topic_id = mock_database()

    # BUG: this returns nothing but I add messages in mock_database()
    maybe_messages = database.get_messages(chat_id)
    if maybe_messages is None:
        raise Exception(f"No conversation with id {chat_id} found")

    messages = [Message(**message) for message in maybe_messages]
    print("Messages so far:", messages, end="\n\n")

    response = await chat_completion(topic_id, messages)
    messages.append(response)
    database.add_message(chat_id, response.role, response.content)
    print("Response:", response, end="\n\n")

    summary_response = await chat_summary(chat_id)
    if summary_response is None:
        raise Exception(f"No conversation with id {chat_id} found")
    print("Summary of conversation:", summary_response, end="\n\n")
    database.add_convo_summary(summary_response.summary, topic_id)

    topic_summary_response = await topic_summary(topic_id)
    print("Summary of topic:", topic_summary_response, end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())
