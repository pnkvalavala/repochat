from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from .utils import model_prompt, custom_que_prompt

def response_chain(db, llm):
    retriever = db.as_retriever()
    search_kwargs = {
        "k": 3,
        "distance_metric": "cos"
    }

    retriever.search_kwargs.update(search_kwargs)

    memory = ConversationBufferMemory(
        memory_key='chat_history',
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