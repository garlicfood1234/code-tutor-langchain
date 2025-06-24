import json
import streamlit as st
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

def add_curriculum_to_db(name, description, curriculum):

    init_curriculum()
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)
    curriculum_path = DATA_DIR / "curriculums.json"

    with open(curriculum_path, "r", encoding="utf-8") as f:
        curriculum_data = json.load(f)
    
    if st.session_state.user_id not in curriculum_data:
        curriculum_data[st.session_state.user_id] = {}

    curriculum_data[st.session_state.user_id][name] = {
        "description": description,
        "curriculum": curriculum
    }
    
    with open(curriculum_path, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, ensure_ascii=False, indent=4)

st.button("커리큘럼 추가", on_click=add_curriculum_to_db, args = ("test", "test", "test"))








