import time
import streamlit as st

from repochat.utils import init_session_state
from repochat.git import git_form
from repochat.db import vector_db, load_to_db
from repochat.models import hf_embeddings, code_llama
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

try:
    db_name, st.session_state['git_form'] = git_form(st.session_state['repo_path'])

    if st.session_state['git_form']:
        with st.spinner('Loading the contents to database. This may take some time...'):
            st.session_state["chroma_db"] = vector_db(
                hf_embeddings(),
                load_to_db(st.session_state['repo_path'])
            )

        st.session_state["db_loaded"] = True
except TypeError:
    pass

if st.session_state["db_loaded"]:
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
                qa = response_chain( 
                    db=st.session_state["chroma_db"],
                    llm=code_llama()
                )

                result = qa({"question": prompt, "chat_history": st.session_state['messages']})
            for chunk in result['answer'].split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})