import streamlit as st
import time

def clear_msg(type: str, msg: str):
    tmp = getattr(st, type)(msg)
    time.sleep(2)
    tmp.empty()