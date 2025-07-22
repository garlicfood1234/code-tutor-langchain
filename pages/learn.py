# 커리큘럼 선택하면, 여기서 이제 학습을 진행하고 그걸 또 ai가 도와주는 페이지임
import streamlit as st
import json
from pathlib import Path
from function import *

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"

def main() : 
    if 'user_id' not in st.session_state : 
        st.switch_page("pages/login.py")
    
    if 'selected_curriculum' not in st.session_state : 
        st.switch_page("pages/curriculum.py")

    curriculums = load_curriculum()[st.session_state.user_id]
    st.session_state.learning_curriculum = curriculums[st.session_state.selected_curriculum]

    st.title(f"커리큘럼 학습")
    st.subheader(f"{st.session_state.selected_curriculum}")

    curriculum_data = load_curriculum()[st.session_state.user_id][st.session_state.selected_curriculum]

    for day, day_data in curriculum_data.items():
        col1, col2 = st.columns([3, 1])

        with col1 : 
            st.subheader(f"{day}")
            st.markdown(f"{day_data['title']}: {day_data['description']}")
        
        with col2 : 
            if st.button("선택", key=f"select_{day}"):
                st.session_state.selected_day = day
                st.switch_page("pages/learn_page.py")
        
        st.divider()
    
            
'''
커리큘럼 학습 페이지 구성

AI를 통해 커리큘럼의 매 Day 학습주제를 가지고 아래와 같은 구조화된 JSON 출력 받기.

예시: 파이썬을 처음 접하고 print()에 대해 배우는 날인 경우

subtitle: 문단 제목
content: 문단 내용
example: 예제 코드
example_input: 예제 코드 입력값
example_output: 예제 코드 출력값
quiz: 퀴즈나 실습 문제

{
    {
        "subtitle": "파이썬 설치 및 개발 환경 셋팅",
        "content": "파이썬을 설치해봅시다. (설치 방법 어쩌구저쩌구)",
        "example": None,
        "example_input": None,
        "example_output": None,
        "quiz": None,
    },
    {
        "subtitle": "파이썬 print() 사용",
        "content": "파이썬에서 print()는 특정 내용을 출력하는 함수입니다. 사용법은 (어쩌구저쩌구)",
        "example": "print("Hello, World!")",
        "example_input": None,
        "example_output": "Hello, World!",
        "quiz": "print() 함수를 사용하여 `안녕하세요`를 출력해 보세요.",
    }
}
'''

main()