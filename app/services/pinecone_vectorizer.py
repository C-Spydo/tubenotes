from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from ..constants import PINECONE_API_KEY, PINCONE_INDEX
from ..models import StockData
from ..extensions import session


def get_pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    spec = ServerlessSpec(cloud='aws', region='us-east-1')  

    index_name = PINCONE_INDEX
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=768,
            spec=spec  
            )

    index = pc.Index(index_name)

    return index

def upsert_documents(documents: tuple[str, str, dict]):
    index = get_pinecone_index()

    character_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    for id, content, metadata in documents:
        chunks = character_splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            embedding = embedder.embed_documents([chunk])[0]
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_index"] = i
            index.upsert([(f"{id}_{i}", embedding, {"text": chunk, **chunk_metadata})])

