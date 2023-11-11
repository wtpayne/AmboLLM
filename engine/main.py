import asyncio
from common import Message
from chat_completion import chat_completion
from chat_summary import chat_summary
from topic_summary import topic_summary

messages = [
    Message(role="system", content="You are a helpful assistant."),
    Message(role="user", content="Hello, who are you?"),
]


async def main():
    response = await chat_completion(messages)
    messages.append(response)
    print(response)

    summary_response = await chat_summary("chat_id", "topic_id", messages)
    print(summary_response)

    topic_summary_response = await topic_summary(
        "topic_id", [Message(role="user", content=summary_response.summary)]
    )
    print(topic_summary_response)


if __name__ == "__main__":
    asyncio.run(main())
