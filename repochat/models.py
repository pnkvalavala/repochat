from langchain.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def hf_embeddings():
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-mpnet-base-v2",
    )

def code_llama():
    callbackmanager = CallbackManager([StreamingStdOutCallbackHandler()])
    llm = LlamaCpp(
        model_path="./models/codellama-7b.Q4_K_M.gguf",
        n_ctx=2048,
        max_tokens=200,
        n_gpu_layers=1,
        f16_kv=True,
        callback_manager=callbackmanager,
        verbose=True,
        use_mlock=True
    )
    return llm