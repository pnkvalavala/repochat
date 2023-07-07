import time
import streamlit as st

from repochat.utils import init_session_state
from repochat.credentials import credentials
from repochat.git import git_form
from repochat.db import vector_db, load_to_db
from repochat.models import openai_embeddings
from repochat.chain import response_chain

init_session_state()

st.set_page_config(
    page_title="RepoChat",
    page_icon="💻",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/pavanvnk/repochat/issues",
        'About': "No need to worry if you can't understand GitHub code or repositories anymore! Introducing RepoChat, where you can effortlessly chat and discuss all things related to GitHub repositories."
    }
)

st.markdown(
    "<h1 style='text-align: center;'>RepoChat</h1>",
    unsafe_allow_html=True
)

credentials()

if st.session_state["auth_ok"]:
    try:
        db_name = git_form(st.session_state['repo_path'])

        st.session_state["db_path"] = f"hub://{st.session_state['al_org_name']}/{db_name}"

        with st.spinner('Loading the contents to database. This may take some time...'):
            vector_db(
                st.session_state["db_path"],
                st.session_state["al_token"],
                openai_embeddings(st.session_state["openai_token"]),
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
                    st.session_state["db_path"], 
                    openai_embeddings(st.session_state["openai_token"]),
                    st.session_state["ai21_token"],
                    st.session_state["al_token"]
                )

                result = qa({"question": prompt, "chat_history": st.session_state['messages']})
            for chunk in result['answer'].split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})