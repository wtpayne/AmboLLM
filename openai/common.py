from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    """A message in the conversation.

    Role is either "system" for the prompt, "user" for user responses, or "assistant" for the model's responses.
    """

    role: str
    content: str


@dataclass
class ChatSummary:
    """
    A summary of the chat for a given topic
    """

    topic_id: str
    chat_id: str
    summary: str


@dataclass
class TopicSummary:
    """
    A summary of all the chat summaries for a given topic
    """

    topic_id: str
    summary: str
