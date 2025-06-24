import streamlit as st
import json
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"

# 유저 커리큘럼 목록을 읽어서 반환하는 함수
def load_curriculum():
    if curriculum_path.exists():
        with open(curriculum_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def add_curriculum():
    st.switch_page("pages/add_curriculum.py")

def display_curriculum_list(user_id: str):
    curriculums = load_curriculum()
        
    st.subheader("커리큘럼 목록")

    st.button("커리큘럼 추가", on_click=add_curriculum)

    print("커리큘러 추가 버튼 출력")

    if curriculums == {} or curriculums[user_id] == {}:
        st.warning("커리큘럼이 없습니다.")
        return
    
    # 각 커리큘럼을 카드 형태로 표시
    for idx, (curriculum_id, curriculum_data) in enumerate(curriculums[user_id].items()):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{curriculum_id}**")
                st.markdown(f"설명: {curriculum_data.get('description', '설명 없음')}")
            
            with col2:
                if st.button("선택", key=f"select_{idx}"):
                    st.session_state.selected_curriculum = curriculum_id
                    st.switch_page("pages/learn.py")
            
            st.divider()

def main() : 
    if not st.session_state.user_id:
        st.switch_page("pages/signin.py")
        return
    
    display_curriculum_list(st.session_state.user_id)