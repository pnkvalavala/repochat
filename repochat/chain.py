import streamlit as st
from langchain.vectorstores import DeepLake
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from .utils import model_prompt, custom_que_prompt

def response_chain(embeddings, al_token, llm):
    db = DeepLake(
        dataset_path=st.session_state["db_path"],
        embedding_function=embeddings,
        read_only=True,
        token=al_token
    )

    retriever = db.as_retriever()
    search_kwargs = {
        "k": 3,
        "fetch_k": 30,
        "distance_metric": "cos",
        "maximal_marginal_relevance": True
    }

    retriever.search_kwargs.update(search_kwargs)

    memory = ConversationBufferMemory(
        memory_key='history',
        return_messages=True
    )

    model_template = model_prompt()
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=model_template
    )
    question_prompt = PromptTemplate.from_template(custom_que_prompt())

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=retriever, 
        memory=memory,
        chain_type='stuff',
        verbose=True,
        combine_docs_chain_kwargs={
            'prompt': QA_CHAIN_PROMPT
        },
        condense_question_prompt=question_prompt
    )

    return qa