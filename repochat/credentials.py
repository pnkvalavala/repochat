import streamlit as st
import requests

from .constants import *

def credentials():
    with st.sidebar:
        openai_token=None
        hf_token=None
        hf_endpoint=None
        st.title("Authentication", help=AUTHENTICATION_HELP)
        embedding_option = st.selectbox('Embeddings', ['OpenAI', 'Hugging Face'])
        llm_option = st.selectbox('LLM', ['GPT-3.5', 'Hugging Face Models'])
        with st.form("tokens"):
            if embedding_option == 'OpenAI' or llm_option == 'GPT-3.5':
                openai_token = st.text_input(
                    "OpenAI API",
                    type="password",
                    help=OPENAI_HELP,
                    placeholder="This field is mandatory"
                )
            if llm_option == 'Hugging Face Models':
                hf_endpoint = st.text_input(
                    "Hugging Face Endpoint",
                    type="password",
                    help=HF_ENDPOINT,
                    placeholder="This field is mandatory"
                )
                hf_token = st.text_input(
                    "Hugging Face Token",
                    type="password",
                    help=HF_TOKEN,
                    placeholder="This field is mandatory"
                )
            al_token = st.text_input(
                "Activeloop Token",
                type="password",
                help=ACTIVELOOP_TOKEN,
                placeholder="This field is mandatory"
            )
            submit_tokens = st.form_submit_button("Submit")
    
    if submit_tokens:
        with st.spinner("Hang tight, validating the tokens..."):
            if((embedding_option=='OpenAI' or llm_option=='GPT-3.5') and openai_token==""):
                st.error("Enter OpenAI API Key")
                st.stop()
            if((llm_option=='Hugging Face Models') and (hf_token=="" or hf_endpoint=="")):
                st.error("Enter Hugging Face Credentials")
                st.stop()
            if not(al_token):
                st.error("Enter Activeloop API Key")
                st.stop()
            if check_al(al_token):
                st.session_state["al_token"] = al_token
                if check_openai(openai_token):
                    st.session_state["openai_token"] = openai_token
                st.session_state["hf_token"] = hf_token
                st.session_state["hf_endpoint"] = hf_endpoint
                st.session_state["auth_ok"] = True
                st.success("Enter GitHub Repository Link")
    return embedding_option, llm_option

def check_openai(openai_token):
    if openai_token==None:
        return True
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_token}',
    }
    response = requests.get("https://api.openai.com/v1/engines", headers=headers)
    if response.status_code == 200:
        return True
    st.error("Enter valid OpenAI token")
    st.stop()

def check_al(al_token):
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {al_token}"
    }
    response = requests.get("https://app.activeloop.ai/api/user/profile", headers=headers)
    profile_data = response.json()

    if profile_data["name"] != "public":
        al_org_name = profile_data["name"]
        st.session_state["al_org_name"] = al_org_name
        return True
    st.error("Enter valid Activeloop token")
    st.stop()