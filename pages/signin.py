# 0_sign_in.py
import streamlit as st
import json
from pathlib import Path

import hashlib

# 페이지 설정
st.set_page_config(
    page_title="로그인",
)

from function import style

st.markdown(style, unsafe_allow_html=True)

# 데이터 저장 경로 설정
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_PROFILE_PATH = DATA_DIR / "user_profiles.json"

# 사용자 정보 파일을 읽어와 딕셔너리로 반환하는 함수
def load_user_profiles():
    if USER_PROFILE_PATH.exists():
        with open(USER_PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}}

# 사용자 인증 함수: 등록된 ID와 비번이 입력된 값과 일치해야함
def auth_user(username, password) : 
    profiles = load_user_profiles()
    
    if username in profiles["users"] : 
        if profiles["users"][username]["pw"] == password : 
            return True
        else : 
            return False
    
    return False


def main():

    if "user_id" in st.session_state and st.session_state.user_id:
        st.switch_page("pages/curriculum.py")
        return
    
    # 페이지 제목 출력
    st.title("로그인")

    # 안내 문구 출력
    st.markdown("""
    서비스를 이용하려면 로그인하십시오.
    """)

    # 로그인 폼 시작
    with st.form("login_form"):
        st.header("로그인")  # 로그인 폼 제목

        # 사용자 입력 필드: ID와 비밀번호
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        # 버튼을 두 열로 나누어 배치
        col1, col2 = st.columns(2)
        with col1:
            # 로그인 버튼
            login_submitted = st.form_submit_button("로그인")
        with col2:
            # 회원가입 버튼 클릭 시 회원가입 페이지로 이동
            if st.form_submit_button("회원가입"):
                st.switch_page("pages/signup.py")
        
        # 로그인 폼 검사
        if login_submitted : 
            if not username or not password : 
                st.error("입력란이 올바르지 않습니다.")
            elif auth_user(username, hashlib.sha256(password.encode('utf-8')).hexdigest()) : 
                st.session_state.user_id = username
                st.session_state.logged_in = True
                st.success("로그인 성공")
                st.switch_page("pages/curriculum.py")
            else : 
                st.error("입력란이 올바르지 않습니다.")

if __name__ == "__main__":
    main()