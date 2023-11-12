from sqlitedict import SqliteDict
import uuid

db = SqliteDict("councilBotDatabase.db")
questions = SqliteDict("councilBotDatabase.db", tablename="questions", autocommit=True)
convo_summaries = SqliteDict(
    "councilBotDatabase.db", tablename="convo_summaries", autocommit=True
)
questions_summaries = SqliteDict(
    "councilBotDatabase.db", tablename="questions_summaries", autocommit=True
)
conversation = SqliteDict(
    "councilBotDatabase.db", tablename="conversation", autocommit=True
)
user = SqliteDict("councilBotDatabase.db", tablename="user", autocommit=True)


def ensure_user_and_topic(user_id, topic_id):
    """
    Ensure that user exists and is associated with topic_id

    """
    user[user_id] = {'conversation': topic_id}


# User table


def add_user(user_id):
    value = {'conversation': []}
    user[user_id] = value
    return id


def add_user_conversation(user_id, question_id):
    conversation_id = create_conversation(question_id, user_id)
    user[user_id]["conversations"].append({"conversation_id": conversation_id})
    return conversation_id


def get_user_conversations(user_id):
    try:
        return user[user_id]
    except:
        return None


# Conversation Table


def create_conversation(question_id, user_id):
    id = str(uuid.uuid4())
    value = {"question_id": question_id, "user_id": user_id, "messages": []}
    conversation[id] = value
    return id


def get_conversation(conversation_id):
    try:
        return conversation[conversation_id]
    except:
        return None


def get_conversation_question_id(conversation_id):
    try:
        return conversation[conversation_id]["question_id"]
    except:
        return None


def get_conversation_user_id(conversation_id):
    try:
        return conversation[conversation_id]["user_id"]
    except:
        return None


def add_message(conversation_id, role, content):
    message = {"role": role, "content": content}
    messages = conversation[conversation_id]["messages"]
    messages.append(message)
    copy = conversation[conversation_id]
    copy["messages"] = messages
    conversation[conversation_id] = copy


def get_messages(conversation_id):
    try:
        return conversation[conversation_id]["messages"]
    except:
        return None


# Questions Table


def add_question(question_string):
    id = str(uuid.uuid4())
    value = {"question": question_string}
    questions[id] = value
    return id


def get_questions():
    questions_list = []
    for key, value in questions.items():
        questions_list.append({"id": key, "text": value["question"]})
    return questions_list


def delete_question(id):
    try:
        del questions[id]
        print("Question Deleted")
    except:
        print("Question not found")


def get_question(id):
    try:
        return questions[id]
    except:
        return None


# Convo Summaries table


def add_convo_summary(summary, question_id):
    id = str(uuid.uuid4())
    value = {"question_id": question_id, "summary": summary}
    convo_summaries[id] = value
    return id


def get_summaries_for_question(question_id):
    summaries_list = []
    for key, value in convo_summaries.items():
        if question_id == value["question_id"]:
            summaries_list.append(
                {
                    "id": key,
                    "question_id": value["question_id"],
                    "summary": value["summary"],
                }
            )
    return summaries_list


def delete_convo_summary(id):
    try:
        del convo_summaries[id]
        print("Summary Deleted")
    except:
        print("Summary not found")


def get_convo_summary(id):
    try:
        return convo_summaries[id]
    except:
        return None


# Question summaries table


def add_question_summary(summary, question_id):
    id = str(uuid.uuid4())
    value = {"question_id": question_id, "summary": summary}
    questions_summaries[id] = value
    return id


def get_all_question_summaries():
    summaries_list = []
    for key, value in questions_summaries.items():
        summaries_list.append(
            {
                "id": key,
                "question": get_question(value["question_id"]),
                "summary": value["summary"],
            }
        )
    return summaries_list


def get_summary_for_question(question_id):
    for key, value in questions_summaries.items():
        if question_id == value["question_id"]:
            return {
                "id": key,
                "question_id": value["question_id"],
                "summary": value["summary"],
            }
    return None


def delete_question_summary(id):
    try:
        del questions_summaries[id]
        print("Summary Deleted")
    except:
        print("Summary not found")


# EXAMPLE

# Questions
# question_id = add_question("Hi")
# print("Question Added", get_question(question_id))
# print("All questions", get_questions())
# print()

# # ConvoSummaries
# summary_id = add_convo_summary("Hello", question_id)
# summary_id = add_convo_summary("Hola", question_id)
# print()
# print("Question convo summaries", get_summaries_for_question(question_id))
# print()

# # QuestionSummary
# question_summary_id = add_question_summary("Greetings", question_id)
# print("Question summary", get_summary_for_question(question_id))
# print("All questions with their summaries", get_all_question_summaries())
