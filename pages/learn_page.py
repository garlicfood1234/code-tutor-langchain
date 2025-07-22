import streamlit as st
from function import *
import sqlite3

import json

def main() : 
    if "user_id" not in st.session_state or not st.session_state.user_id:
        st.switch_page("pages/signin.py")
    
    if "selected_curriculum" not in st.session_state or not st.session_state.selected_curriculum:
        st.switch_page("pages/curriculum.py")
    
    if "selected_day" not in st.session_state or not st.session_state.selected_day:
        st.switch_page("pages/learn.py")
    
    curriculum_data = load_curriculum()[st.session_state.user_id][st.session_state.selected_curriculum][st.session_state.selected_day]
    st.title(f"{st.session_state.selected_curriculum} - {st.session_state.selected_day}")
    st.header(f"{curriculum_data['title']}")
    st.markdown(f"{curriculum_data['description']}")

    st.divider()

main()