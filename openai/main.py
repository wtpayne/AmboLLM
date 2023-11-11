import asyncio
from chat_completion import chat_completions, Message

messages = [
    Message(role="system", content="You are a helpful assistant."),
    Message(role="user", content="Hello, who are you?"),
]

response = asyncio.run(chat_completions(messages))

print(response)
