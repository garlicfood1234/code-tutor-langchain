import json
import streamlit as st
from pathlib import Path
import sqlite3

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"
USER_PROFILE_PATH = DATA_DIR / "user_profiles.json"

style = """
<style>
:root{
  /* 주요 색상 */
  --primary: #00B3E6;       /* 주요 액션 (진한 민트) */
  --primary-dark: #0099CC;

  /* 사용자 선호색 계열 (#77C4A3 변형들) */
  --accent: #77C4A3;        /* 기본 강조 (연한 그린-민트) */
  --accent-1: #BEE9D6;      /* 밝은 변형 */
  --accent-2: #4EA685;      /* 호버/진한 변형 */
  --accent-3: #2F8B6E;      /* 짙은 강조(아이콘 등) */
  --accent-strong: #77C4A3; /* 액션용 대체 */
  --accent-dark: #3E9776;   /* 호버/액티브 */

  /* RGB 포맷을 따로 두어 반투명에 사용하기 쉬움 */
  --accent-rgb: 119,196,163;

  --bg-page: #F7FBFF;
  --text-primary: #111827;
  --muted: #6B7280;
}

/* 페이지 배경, 컨테이너 중앙 정렬(컨테이너는 max-width로 제한) */
section.main .block-container {
  max-width: 1100px;
  margin: 0 auto;
  padding-left: 24px;
  padding-right: 24px;
  background: var(--bg-page);
}

/* 버튼 전체 스타일 (st.button 계열) */
.stButton>button {
  background: var(--accent) !important;    /* 사용자 선호색으로 버튼 적용 */
  color: #072033 !important;               /* 밝은 버튼엔 진한 텍스트로 대비 확보 */
  height: 48px !important;                 /* 터치영역 최소 48px */
  padding: 0 20px !important;
  border-radius: 8px !important;
  font-weight: 600;
  font-size: 16px;
  border: 1px solid rgba(var(--accent-rgb), 0.12) !important;
}
.stButton>button:hover { background: var(--accent-2) !important; color: #072033 !important; }

/* 텍스트 입력 */
.stTextInput>div>input, .stTextArea>div>textarea {
  height: 44px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #D1D5DB;
  font-size: 15px;
}

/* 카드용 클래스 (HTML로 직접 렌더링해서 사용) */
.card {
  background: #FFFFFF;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(2,6,23,0.06);
  margin-bottom: 12px;
}

/* 강조 배지(사용자 선호색) */
.badge-accent {
  background: var(--accent);
  color: #072033;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 600;
  display: inline-block;
}

/* 섹션 강조(반투명) */
.section-accent {
  background: rgba(var(--accent-rgb), 0.18);
  border-left: 4px solid rgba(var(--accent-rgb), 0.28);
  padding: 12px;
  border-radius: 8px;
}

/* 코드 블럭(스트림릿 pre > code 타겟) */
.stCodeBlock pre, pre {
  background: #0F172A; color: #E6F4FF; padding: 12px; border-radius: 8px; font-size:13px;
}

/* 프로그레스 높이 (커스텀) */
.css-1xt0k9k>div[role="progressbar"]>div>div {
  height: 8px !important;
  border-radius: 4px !important;
  /* 진행바 채움 색상을 사용자 선호색(--accent)으로 설정 */
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent) 100%) !important;
  box-shadow: none !important;
}

/* 보조 텍스트 */
small, .muted { color: var(--muted); font-size:13px; }

/* 채팅 버블 (st.chat_message 내부에 HTML로 버블을 만들면 적용) */
.assistant-bubble {
  background: #F1F5FF;
  padding: 12px;
  border-radius: 12px;
  font-size: 15px;
  max-width: 72%;
  color: var(--text-primary);
}
.user-bubble {
  background: #E6F7F1;
  padding: 12px;
  border-radius: 12px;
  font-size: 15px;
  max-width: 72%;
  color: var(--text-primary);
}
</style>
"""

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
