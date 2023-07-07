import os
import re
import shutil
import subprocess
import streamlit as st

def init_session_state():
    SESSION_DEFAULTS = {
        "messages": [],
        "auth_ok": False,
        "openai_token": None,
        "al_token": None,
        "al_org_name": None,
        "db_path": None,
        "db_loaded": False,
        "ai21_token": None,
        "repo_path": './cloned_repo'
    }

    for keys, values in SESSION_DEFAULTS.items():
        if keys not in st.session_state:
            st.session_state[keys] = values

def url_name(url):
    pattern = r"https?://github.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    if match:
        owner = match.group(1)
        repo = match.group(2)
        return f"{owner}_{repo}"
    else:
        st.error("Enter valid GitHub URL")
        st.stop()

def clone_repo(git_url, repo_path):
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    command = f'git clone {git_url}.git {repo_path} && rm -rf {repo_path}/.git'
    subprocess.run(command, shell=True)