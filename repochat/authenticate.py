import deeplake
import requests
import streamlit as st
from deeplake.util.exceptions import InvalidTokenException, TokenPermissionError
from .utils import clear_msg
from .constants import *

def token_form() -> None:
    with st.sidebar:
        st.title("Authentication", help=AUTHENTICATION_HELP)
        with st.form("authentication"):
            hf_token = st.text_input(
                "Hugging Face Token",
                type="password",
                help=HUGGING_FACE_HELP,
                placeholder="This field is mandatory"
            )
            activeloop_org_name = st.text_input(
                "Activeloop Organization Name",
                type="password",
                help=ACTIVELOOP_ORG_NAME,
                placeholder="This field is mandatory"
            )
            activeloop_token = st.text_input(
                "Activeloop Token",
                type="password",
                help=ACTIVELOOP_TOKEN,
                placeholder="This field is mandatory"
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                authenticate(hf_token, activeloop_org_name, activeloop_token)

def authenticate(hf_token, activeloop_org_name, activeloop_token):
    with st.spinner("Authentifying..."):
        if not(hf_token and activeloop_org_name and activeloop_token):
            st.session_state["auth_ok"] = False
            clear_msg("error", "Enter all credentials")
            return
        if not check_activeloop_token(activeloop_org_name, activeloop_token):
            st.session_state["auth_ok"] = False
            return
    st.session_state["auth_ok"] = True
    st.session_state["hf_token"] = hf_token
    st.session_state["activeloop_token"] = activeloop_token
    st.session_state["activeloop_org_name"] = activeloop_org_name
    clear_msg("success", "Authentification successful!")

def check_activeloop_token(activeloop_org_name, activeloop_token) -> bool:
    dataset_path=f"hub://{activeloop_org_name}/repochat"
    try:
        deeplake.empty(dataset_path, token=activeloop_token, overwrite=True)
        return True
    except TokenPermissionError:
        clear_msg("error", "Invalid Activeloop Username. Please check and try again.")
        return False
    except InvalidTokenException:
        clear_msg("error", "Invalid Activeloop token. Please check your API token and try again.")
        return False

    
def authenticate_git(github_url):
    if not(github_url):
        st.session_state["git_url"] = False
        clear_msg("warning", "Enter GitHub URL")
        st.stop()
    try:
        response = requests.get(github_url)
        if response.status_code == 200:
            clear_msg("success", "GitHub Link loaded successfully!")
            st.session_state["git_url"] = True
            return
        else:
            clear_msg("warning", f"Enter Valid GitHub Repo")
            st.stop()
    except requests.exceptions.MissingSchema:
        clear_msg("warning", "Invalid URL. Please include the scheme (e.g., http://)")
        st.stop()
    
        