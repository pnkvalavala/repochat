import streamlit as st
import requests

from .constants import *

def credentials():
    with st.sidebar:
        st.title("Authentication", help=AUTHENTICATION_HELP)
        with st.form("tokens"):
            openai_token = st.text_input(
                "OpenAI API",
                type="password",
                help=OPENAI_HELP,
                placeholder="This field is mandatory"
            )
            al_token = st.text_input(
                "Activeloop Token",
                type="password",
                help=ACTIVELOOP_TOKEN,
                placeholder="This field is mandatory"
            )
            ai21_token = st.text_input(
                "AI21 Labs Token",
                type="password",
                help=AI21_TOKEN,
                placeholder="This field is mandatory"
            )
            submit_tokens = st.form_submit_button("Submit")
    
    if submit_tokens:
        with st.spinner("Hang tight, validating the tokens..."):
            if not(openai_token and al_token and ai21_token):
                st.error("Enter all credentials")
                st.stop()
            if check_openai(openai_token) and check_al(al_token):
                st.session_state["auth_ok"] = True
                st.session_state["openai_token"] = openai_token
                st.session_state["al_token"] = al_token
                st.session_state["ai21_token"] = ai21_token
                st.success("Enter GitHub Repository Link")

def check_openai(openai_token):
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