import os
import requests
import streamlit as st

from .utils import url_name, clone_repo

def git_form():
    with st.sidebar:
        st.title("GitHub Link")
        with st.form("git"):
            git_url = st.text_input("Enter GitHub Repository Link")
            submit_git = st.form_submit_button("Submit")
    if submit_git:
        with st.spinner("Checking GitHub URL"):
            if not(git_url):
                st.warning("Enter GitHub URL")
                st.stop()
            try:
                response = requests.get(git_url)
                if response.status_code == 200 and url_name(git_url):
                    st.success("GitHub Link loaded successfully!")
                    db_name = url_name(git_url)
                    # db_path = f"hub://{al_org_name}/{db_name}"
                    # if not deeplake.exists(path=db_path, token=al_token):
                    #     deeplake.rename(f"hub://{al_org_name}/check3", db_path, token=al_token)
                else:
                    st.error("Enter Valid GitHub Repo")
                    st.stop()
            except requests.exceptions.MissingSchema:
                st.error("Invalid URL. Please include the scheme (e.g., https://)")
                st.stop()
        
        with st.spinner(f"Cloning {db_name} Repository"):
            repo_path = os.path.join(os.getcwd(), "cloned_repo")
            clone_repo(git_url, repo_path)
            st.success("Cloned successfully!")
            return repo_path, db_name