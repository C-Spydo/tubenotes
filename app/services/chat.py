import jsonpickle
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from app.dtos.chat_setting import ChatSetting
from app.dtos.prompt import Prompt
from app.repository.chat import get_chat_by_id
from app.repository.user import get_user_by_email
from ..enums import ActiveStocks
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from app.helpers import add_record_to_database
from app.models import Chat
from langchain_core.messages import SystemMessage
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from ..constants import PINCONE_INDEX, PINECONE_API_KEY
from flask import abort


def start_chat(request: ChatSetting):
    user = validate_user(request['email'])
    stock = validate_stock(request['stock'])

    chat_memory = create_chat_memory()
    
    langchain_conversation = create_conversation_chain(get_llm(), chat_memory, get_prompt_template(stock))
    ai_response = langchain_conversation.invoke({"question": request['prompt'], "chat_history": chat_memory.load_memory_variables({})["chat_history"]})

    chat = Chat(user_id=user.id, stock=stock, memory=jsonpickle.encode(chat_memory))
    add_record_to_database(chat)

    return {"chat_id": chat.id, "chat_history": chat_memory.load_memory_variables({})["chat_history"] ,"ai_response": ai_response["answer"]}

def prompt_bot(request: Prompt):
    chat = get_chat_by_id(request['chat_id'])
    chat_memory = chat.deserialize_chat_memory()

    langchain_conversation = create_conversation_chain(get_llm(), chat_memory, get_prompt_template(chat.stock))

    ai_response = langchain_conversation.invoke({"question": request['prompt']})

    chat.update_chat_memory(chat_memory)

    return {"chat_id": chat.id, "chat_history": chat_memory.load_memory_variables({})["chat_history"] ,"ai_response": ai_response["answer"]}

def get_llm():
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.3,
        max_tokens=250,
        timeout=3,
        max_retries=2
    )

    return llm


def create_conversation_chain(llm, chat_memory, prompt_template):
    retriever = stock_retriever()

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=chat_memory,
        condense_question_prompt=prompt_template,
        chain_type="stuff"
    )

def stock_retriever():  
    vectorstore = PineconeVectorStore(index_name=PINCONE_INDEX, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    return retriever

def create_chat_memory():
    return ConversationBufferMemory(
            memory_key="chat_history",
            input_key="question",
            return_messages=False,
            ai_prefix="AI",
            human_prefix="User"
        )

def get_system_message(stock):
     return f"""
        You are a chatbot assistant on {stock} stocks.
        You are asked to generate short and accurate answers using the provided context.
        Do not formulate answers—only use the retrieved documents.
        """
    

def get_prompt_template(stock):
    system_message = get_system_message(stock)

    template = (
    f"{system_message}"
    "Combine the chat history and follow up question into "
    "a standalone question. Chat History: {chat_history}"
    "Follow up question: {question}")

    return PromptTemplate.from_template(template)
    
def validate_user(email: str):
    user = get_user_by_email(email)

    if user is None:
        raise abort(404, "User not found")
    
    return user


def validate_stock(stock: str):
    if stock not in ActiveStocks.__members__:
        raise abort(400, f"Invalid stock: {stock}. Available stocks: {', '.join(ActiveStocks.__members__.keys())}")

    return stock
