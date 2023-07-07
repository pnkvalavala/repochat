import streamlit as st

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
            al_org_name = st.text_input(
                "Activeloop Organization Name",
                type="password",
                help=ACTIVELOOP_ORG_NAME,
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
            if not(openai_token or al_token or al_org_name or ai21_token):
                st.error("Enter all credentials")
                st.stop()
        st.session_state["auth_ok"] = True
        st.session_state["openai_token"] = openai_token
        st.session_state["al_token"] = al_token
        st.session_state["al_org_name"] = al_org_name
        st.session_state["ai21_token"] = ai21_token
        st.success("Authentification successful!\n\nNow Enter GitHub Repository Link")
        return st.session_state["openai_token"], st.session_state["al_token"], st.session_state["al_org_name"], st.session_state["ai21_token"]

# S3 deletion error -> Issue
# def check_al_token(al_token, al_org_name) -> bool:
#     dataset_path=f"hub://{al_org_name}/check3"
#     try:
#         deeplake.empty(dataset_path, token=al_token, overwrite=True)
#         return True
#     except TokenPermissionError:
#         st.error("Invalid Activeloop token/username. Please check and try again.")
#         st.stop()
#     except InvalidTokenException:
#         st.error("Invalid Activeloop token. Please check your API token and try again.")
#         st.stop()