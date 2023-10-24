from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceEndpoint

def openai_embeddings(openai_api):
    return OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=openai_api,
        disallowed_special=()
    )

def open_ai(openai_api):
    return ChatOpenAI(
        model="gpt-3.5-turbo", 
        openai_api_key=openai_api
    )

def hf_embeddings():
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-mpnet-base-v2",
    )

def hf_inference(endpoint, hf_token):
    return HuggingFaceEndpoint(
        endpoint_url=endpoint,
        huggingfacehub_api_token=hf_token
    )