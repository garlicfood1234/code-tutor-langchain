import streamlit as st
import json
from pathlib import Path
from function import *

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"

def display_curriculum_list(user_id: str):
    curriculums = load_curriculum()
        
    st.subheader("커리큘럼 목록")

    if st.button("커리큘럼 생성") : 
        st.switch_page("pages/new_curriculum.py")

    if not curriculums.get(user_id):
        st.warning("커리큘럼이 없습니다.")
        return
    
    # 각 커리큘럼을 카드 형태로 표시 (역순)
    for idx, (curriculum_id, curriculum_data) in enumerate(reversed(list(curriculums[user_id].items()))):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{curriculum_id}**")
            
            with col2:
                if st.button("선택", key=f"select_{idx}"):
                    st.session_state.selected_curriculum = curriculum_id
                    st.switch_page("pages/learn.py")
            
            st.divider()

def main() : 
    if "user_id" not in st.session_state or not st.session_state.user_id:
        st.switch_page("pages/signin.py")
    
    display_curriculum_list(st.session_state.user_id)

main()