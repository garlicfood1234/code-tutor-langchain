# 커리큘럼 선택하면, 여기서 이제 학습을 진행하고 그걸 또 ai가 도와주는 페이지임
import streamlit as st
import json
from pathlib import Path
from function import *

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"

def main() : 
    if 'user_id' not in st.session_state : 
        st.switch_page("pages/login.py")
    
    if 'selected_curriculum' not in st.session_state : 
        st.switch_page("pages/curriculum.py")

    curriculums = load_curriculum()[st.session_state.user_id]
    st.session_state.learning_curriculum = curriculums[st.session_state.selected_curriculum]

    st.title(f"커리큘럼 학습")
    st.subheader(f"{st.session_state.selected_curriculum}")

main()