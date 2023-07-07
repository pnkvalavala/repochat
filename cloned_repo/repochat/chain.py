from langchain.llms import AI21
from langchain.vectorstores import DeepLake
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def response_chain(db_path, embeddings, ai21_token, al_token):
    db = DeepLake(
        dataset_path=db_path,
        embedding_function=embeddings,
        read_only=True,
        token=al_token
    )

    retriever = db.as_retriever()
    search_kwargs = {
        "k": 10,
        "fetch_k": 30,
        "distance_metric": "cos",
        "maximal_marginal_relevance": True
    }

    retriever.search_kwargs.update(search_kwargs)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    model = AI21(
        model="j2-ultra",
        temperature=0.4,
        maxTokens=2048,
        ai21_api_key=ai21_token
    )

    qa = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        chain_type="stuff",
        memory=memory,
        verbose=True
    )

    return qa