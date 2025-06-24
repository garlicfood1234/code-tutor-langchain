import json
import streamlit as st
from pathlib import Path

def add_curriculum_to_db(name, description, curriculum):
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)
    curriculum_path = DATA_DIR / "curriculums.json"

    with open(curriculum_path, "r", encoding="utf-8") as f:
        curriculum_data = json.load(f)

    curriculum_data[st.session_state.user_id][name] = {
        "description": description,
        "curriculum": curriculum}
    
    with open(curriculum_path, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, ensure_ascii=False, indent=4)

st.button("커리큘럼 추가", on_click=add_curriculum_to_db, args = ("test", "test", "test"))








