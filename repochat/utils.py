import re
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
        "ai21_token": None
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
    try:
        subprocess.run(['git', 'clone', git_url, repo_path])
    except Exception:
        st.warning("Refresh the page")
        st.stop()