import json
import streamlit as st
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"
USER_PROFILE_PATH = DATA_DIR / "user_profiles.json"

# 사용자 정보 파일을 읽어와 
def load_user_profiles() : 
    # 파일이 존재하는지 확인 후 열어서 내용 읽기
    if USER_PROFILE_PATH.exists() : 
        with open(USER_PROFILE_PATH, "r", encoding = "utf-8") as f: 
            return json.load(f)
    
    return {"users": {}}

def init_user_profiles():
    # JSON 파일이 존재하지 않으면 초기화를 수행
    if not USER_PROFILE_PATH.exists():
        # 파일을 쓰기 모드로 열고 저장 준비
        with open(USER_PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f, ensure_ascii=False, indent=4)

# 사용자 정보 파일에 저장하는 함수
def save_user_profile(user_id, profile_data):
    profiles = load_user_profiles()
    profiles["users"][user_id] = profile_data

    # 파일에 정보 저장
    with open(USER_PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)

def load_user_profile(user_id):
    profiles = load_user_profiles()
    return profiles.get("users", {}).get(user_id)

def init_curriculum():
    # JSON 파일이 존재하지 않으면 초기화를 수행
    if not curriculum_path.exists():
        # 파일을 쓰기 모드로 열고 저장 준비
        with open(curriculum_path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)

def load_curriculums() : 
    # 파일이 존재하는지 확인 후 열어서 내용 읽기
    if curriculum_path.exists() : 
        with open(curriculum_path, "r", encoding = "utf-8") as f: 
            return json.load(f)
    
    return {}

def save_curriculums(curriculum_data) : 
    with open(curriculum_path, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, ensure_ascii=False, indent=4)
