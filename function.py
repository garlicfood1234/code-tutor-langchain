import json
import streamlit as st
from pathlib import Path
import sqlite3

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"
USER_PROFILE_PATH = DATA_DIR / "user_profiles.json"

def init_db() : 
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()

    cursor = cursor.execute("CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, curriculum_title TEXT, user_ai TEXT, chat_history TEXT)") # user_ai: 챗봇이 친 건지 유저가 친 건지 구분, user_id 유저 id, chat_history: 채팅 히스토리
    conn.commit()
    conn.close()

def save_chat_history(user_id, curriculum_title, user_ai, chat_history) : 
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO chat_history (user_id, curriculum_title, user_ai, chat_history) VALUES (?, ?, ?, ?)", (user_id, curriculum_title, user_ai, chat_history))
    conn.commit()
    conn.close()

def load_chat_history(user_id, curriculum_title) : 
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history WHERE user_id = ? AND curriculum_title = ?", (user_id, curriculum_title))
    temp = cursor.fetchall()
    conn.close()
    return temp

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
    

def save_curriculums(curriculum_data) : 
    with open(curriculum_path, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, ensure_ascii=False, indent=4)
