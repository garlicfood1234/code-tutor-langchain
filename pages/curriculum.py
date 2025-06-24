import streamlit as st
import json
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"

def init_curriculum() : 
    # JSON 파일이 존재하지 않으면 초기화를 수행
    if not curriculum_path.exists() : 
        # 파일을 쓰기 모드로 열고 저장 준비
        with open(curriculum_path, "w", encoding = "utf-8") as f : 
            json.dump({}, f, ensure_ascii = False, indent = 4)

# 유저 커리큘럼 목록을 읽어서 반환하는 함수
def load_curriculum():
    if curriculum_path.exists():
        with open(curriculum_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else : 
        init_curriculum()
    return {}

def display_curriculum_list(user_id: str):
    curriculums = load_curriculum()
        
    st.subheader("커리큘럼 목록")

    if st.button("커리큘럼 생성") : 
        st.switch_page("pages/new_curriculum.py")

    if not curriculums.get(user_id):
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
    if "user_id" not in st.session_state or not st.session_state.user_id:
        st.switch_page("pages/signin.py")
    
    display_curriculum_list(st.session_state.user_id)

main()