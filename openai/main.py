import asyncio
from common import Message
from chat_completion import chat_completion
from chat_summary import chat_summary

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


asyncio.run(main())
