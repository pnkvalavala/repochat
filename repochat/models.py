from langchain.embeddings.openai import OpenAIEmbeddings

def openai_embeddings(openai_api):
    return OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=openai_api,
        disallowed_special=()
    )

# Add other open-source LLMs