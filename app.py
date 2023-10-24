import streamlit as st

from repochat.utils import init_session_state
from repochat.credentials import credentials
from repochat.git import git_form
from repochat.db import vector_db, load_to_db
from repochat.models import *
from repochat.chain import response_chain

init_session_state()

st.set_page_config(
    page_title="RepoChat",
    page_icon="💻",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/pnkvalavala/repochat/issues",
        'About': "No need to worry if you can't understand GitHub code or repositories anymore! Introducing RepoChat, where you can effortlessly chat and discuss all things related to GitHub repositories."
    }
)

st.markdown(
    "<h1 style='text-align: center;'>RepoChat</h1>",
    unsafe_allow_html=True
)

embedding_option, llm_option = credentials()

if st.session_state["auth_ok"]:
    try:
        db_name, st.session_state['git_form'] = git_form(st.session_state['repo_path'])

        if st.session_state['git_form']:
            st.session_state["db_path"] = f"hub://{st.session_state['al_org_name']}/{db_name}"

            if embedding_option=='OpenAI':
                st.session_state['embeddings'] = openai_embeddings(st.session_state["openai_token"])
            else:
                st.session_state['embeddings'] = hf_embeddings()
            
            if llm_option=='GPT-3.5':
                st.session_state['llm'] = open_ai(st.session_state["openai_token"])
            else:
                st.session_state['llm'] = hf_inference(st.session_state["hf_endpoint"], st.session_state["hf_token"])

            with st.spinner('Loading the contents to database. This may take some time...'):
                st.session_state["deeplake_db"] = vector_db(
                    st.session_state['embeddings'],
                    load_to_db(st.session_state['repo_path'])
                )

            st.session_state["db_loaded"] = True
    except TypeError:
        pass

if st.session_state["db_loaded"]:
    st.session_state["qa"] = response_chain( 
        db=st.session_state["deeplake_db"],
        llm=st.session_state['llm']
    )
    
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your query"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Generating response..."):
                result = st.session_state["qa"]({"question": prompt, "chat_history": st.session_state['messages']})
                st.write(result['answer'])
        st.session_state["messages"].append({"role": "assistant", "content": result['answer']})