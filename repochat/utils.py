import os
import re
import shutil
import subprocess
import streamlit as st

def init_session_state():
    SESSION_DEFAULTS = {
        "messages": [],
        "chroma_db": None,
        "db_loaded": False,
        "repo_path": './cloned_repo',
        "git_form": False,
        "qa": None,
        "db_name": None
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
    
    git_url = git_url.replace(".git", "")

    command = f'git clone {git_url}.git {repo_path} && rm -rf {repo_path}/.git'
    subprocess.run(command, shell=True)

def prompt_format(system_prompt, instruction):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<SYS>>\n", "\n<</SYS>>\n\n"
    SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

def model_prompt():
    system_prompt = """You are a helpful assistant, you have good knowledge in coding and you will use the provided context to answer user questions with detailed explanations.
    Read the given context before answering questions and think step by step. If you can not answer a user question based on the provided context, inform the user. Do not use any other information for answering user"""
    instruction = """
    Context: {context}
    User: {question}"""
    return prompt_format(system_prompt, instruction)

def custom_que_prompt():
    que_system_prompt = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question and give only the standalone question as output in the tags <question> and </question>.
    """

    instr_prompt = """Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    return prompt_format(que_system_prompt, instr_prompt)