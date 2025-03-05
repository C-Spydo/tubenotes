import jsonpickle
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from app.dtos.chat_setting import ChatSetting
from app.dtos.prompt import Prompt
from app.repository.chat import get_chat_by_id
from app.repository.user import get_user_by_username
from ..extensions.database import session
from ..enums import ActiveStocks
from langchain.chains.conversation.base import ConversationChain
from langchain.chains import ConversationalRetrievalChain
from app.helpers import add_record_to_database, create_response
from app.models import User, Chat
from langchain_core.messages import SystemMessage
from langchain.prompts import PromptTemplate
from flask import abort



def start_chat(request: ChatSetting):
    user = validate_user(request['username'])
    stock = validate_stock(request['stock'])

    chat_memory = create_chat_memory()
    chat_memory.chat_memory.add_message(SystemMessage(content=f"You are a {request['character_description']} named {request['character_name']}, play the role and engage this user in a conversation"))
    
    langchain_conversation = create_conversation_chain(get_llm(), chat_memory, stock)
    ai_response = langchain_conversation.predict(input=request['prompt'])

    chat = Chat(user_id=user.id, character_name=request['character_name'], stock=request['stock'], memory=jsonpickle.encode(chat_memory))
    add_record_to_database(chat)

    return {"chat_id": chat.id, "chat_history": chat_memory.load_memory_variables({})["history"] ,"ai_response": ai_response}

def prompt_bot(request: Prompt):
    chat = get_chat_by_id(request['chat_id'])
    chat_memory = chat.deserialize_chat_memory()

    langchain_conversation = create_conversation_chain(get_llm(), chat_memory, chat.stock)
    ai_response = langchain_conversation.predict(input=request['prompt'])

    chat.update_chat_memory(chat_memory)

    return {"chat_id": chat.id, "chat_history": chat_memory.load_memory_variables({})["history"] ,"ai_response": ai_response}

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

def create_conversation_chain(llm, chat_memory, stock):


    retriever = stock_retriever(stock)
    return ConversationalRetrievalChain(
        llm=llm,
        retriever=retriever,
        memory=chat_memory
    )


def stock_retriever(stock):
    #Assuming this is where the RAG magic happens with TextLoader, Embeddings , Pinecone, etc
    #returns a vectorstore.as_retriever()

    file_path = f"docs/{stock}.txt"
    #
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"No document found for stock: {stock}")


    return None

def create_chat_memory():
    return ConversationBufferMemory(
            memory_key="history",
            return_messages=False,
            ai_prefix="AI",
            human_prefix="User"
        )

def validate_user(username: str):
    user = get_user_by_username(username)

    if user is None:
        raise abort(404, "User not found")
    
    return user


def validate_stock(stock: str):
    if stock not in ActiveStocks.__members__:
        raise abort(400, f"Invalid stock: {stock}. Available stocks: {', '.join(ActiveStocks.__members__.keys())}")

    return stock
