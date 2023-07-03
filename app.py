import streamlit as st
import random
import time
from repochat.authenticate import token_form, authenticate_git
from repochat.utils import clear_msg

st.title("RepoChat")

if "auth_ok" not in st.session_state:
    st.session_state["auth_ok"] = False

token_form()

with st.sidebar:
    st.title("GitHub Link")
    with st.form("git"):
        git_url = st.text_input("Enter GitHub Repository Link")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not st.session_state["auth_ok"]:
                clear_msg("error", "First Enter Credentials")
                st.stop()
            authenticate_git(git_url)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": full_response})