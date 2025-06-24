# 라이브러리 추가
import streamlit as st
import json
from pathlib import Path
import hashlib


# 페이지 설정
st.set_page_config(
    page_title = "회원 가입",
)

# 사용자 데이터를 저장할 폴더 경로 설정
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True) # 폴더가 없으면 생성

# 사용자 정보가 저장될 JSON 파일 경로 정의
USER_PROFILE_PATH = DATA_DIR / "user_profiles.json"

# 사용자 정보 파일 없는 경우 초기화
def init_user_profiles() : 
    # JSON 파일이 존재하지 않으면 초기화를 수행
    if not USER_PROFILE_PATH.exists() : 
        # 파일을 쓰기 모드로 열고 저장 준비
        with open(USER_PROFILE_PATH, "w", encoding = "utf-8") as f : 
            json.dump({"users": {}}, f, ensure_ascii = False, indent = 4)

# 사용자 정보 파일을 읽어와 
def load_user_profiles() : 
    # 파일이 존재하는지 확인 후 열어서 내용 읽기
    if USER_PROFILE_PATH.exists() : 
        with open(USER_PROFILE_PATH, "r", encoding = "utf-8") as f: 
            return json.load(f)
    
    return {"users": {}}

# 사용자 정보 파일에 저장하는 함수
def save_user_profile(user_id, profile_data) :
    profiles = load_user_profiles()
    profiles["users"][user_id] = profile_data

    # 파일에 정보 저장
    with open(USER_PROFILE_PATH, "w", encoding = "utf-8") as f : 
        json.dump(profiles, f)

def main() : 
    st.title("회원 가입")

    # 회원가입 입력 form 생성
    with st.form("signup_form") : 
        # 폼 상단에 제목 출력
        st.header("계정을 생성하세요.")

        # 폼에 입력받을 항목들 정의
        id = st.text_input("아이디")
        pw = st.text_input("비밀번호", type="password")
        confirm_pw = st.text_input("비밀번호 확인", type = "password")
        age = st.number_input("나이 (만 나이)", min_value = 4, max_value = 125, step = 1, value = 14)
        language_level = st.selectbox(
            "학습 단계",
            ["최하", "하", "중하", "중", "중상", "상", "최상"]
        )
        goal = st.text_input("학습 목표", placeholder="예: 파이썬 langchain을 사용하여 나만의 챗봇 만들기")
        comment = st.text_input("AI 코치가 추가적으로 고려해야 할 사항", placeholder="예: 나는 이해력이 떨어지므로 쉽게 설명해 주세요")

        # 버튼을 좌우 두 열로 분할하여 배치
        col1, col2 = st.columns(2)
        with col1 : 
            sign_up_submitted = st.form_submit_button("가입")
        with col2 : 
            if st.form_submit_button("돌아가기") : 
                st.switch_page("main.py")

        if sign_up_submitted : 
            # 모든 필수 입력값이 채워졌는지 확인
            if not all([id, pw, confirm_pw, age, language_level, goal]) : 
                # 에러 표시
                st.error("필수 입력란이 비어있습니다.")
            # 비밀번호가 확인 비밀번호와 일치하는지 확인
            elif pw != confirm_pw : 
                st.error("confirm_pw의 값이 올바르지 않습니다.")
            else : 
                profiles = load_user_profiles()

                if id in profiles["users"] : 
                    st.error("id의 값은 중복되지 않아야 합니다.")
                elif len(id) < 5 : 
                    st.error("id의 길이는 5 이상이어야 합니다.")
                elif len(pw) < 8 : 
                    st.error("pw의 길이는 8 이상이어야 합니다.")
                elif age < 14 : 
                    st.error("age의 값은 14 이상이어야 합니다.")
                else : 
                    # 사용자 정보를 딕셔너리로 정리
                    profile_data = {
                        "id" : id,
                        "pw" : hashlib.sha256(pw.encode('utf-8')).hexdigest(),  # 비밀번호를 해시로 저장
                        "age" : age,
                        "language_level": language_level,
                        "goal": goal
                    }

                    save_user_profile(id, profile_data)

                    # 성공 메시지 표시 및 세션 상태 설정
                    st.session_state.user_id = id
                    st.session_state.profile_setup = True

                    st.switch_page("main.py")

if __name__ == "__main__" : 
    init_user_profiles()
    main()