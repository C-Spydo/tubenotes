from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from app.repository.user import get_user_by_username
from ..extensions.database import session
from langchain.chains.conversation.base import ConversationChain
from app.helpers import add_record_to_database, create_response
from app.models import User
from langchain.prompts import PromptTemplate
from ..dtos.message_request import MessageRequest
from flask import abort


def fetch_chat_history(username: str):
    user = get_user_by_username(username)

    if user is None:
        user = User(username=username)
        add_record_to_database(user)

    serialized_user = user.serialize()

    chat_memory = serialized_user['chat_memory']

    if chat_memory is not None:
        serialized_user['chat_memory'] = chat_memory.load_memory_variables({})["history"]

    return serialized_user


def prompt_bot(request: MessageRequest):
    user = get_user_by_username(request['username'])

    if user is None:
        raise abort(404, "User not found")

    chat_memory = user.serialize()['chat_memory']

    if chat_memory is None:
        chat_memory = create_chat_memory()
    

    langchain_conversation = ConversationChain(
        llm=get_llm(),
        memory=chat_memory,
        prompt=get_prompt_template(request['system_message'])
    )

    ai_response = langchain_conversation.predict(input=request['prompt'])

    user.save_chat_memory(chat_memory)
    session.commit()

    return {"ai_response": ai_response, "chat_memory": chat_memory.load_memory_variables({})["history"]}

def get_llm():
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.3,
        max_tokens=250,
        timeout=3,
        max_retries=2
    )

    return llm

def get_prompt_template(character: str):
    return PromptTemplate(
        input_variables=["history", "input"],
        template=(
            f"System: {character}, play along with this user, your reponses should be at most 250 words\n\n"
            "The following is a conversation between User and AI:\n\n"
            "{history}\n\n"
            "User: {input}\nAI:"
        )
    )

def create_chat_memory():
    return ConversationBufferMemory(
            memory_key="history",
            return_messages=False,
            ai_prefix="AI",
            human_prefix="User"
        )