import streamlit as st
from function import *
import sqlite3

import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import FewShotChatMessagePromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_chroma import Chroma
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def create_chat_chain(result_dict, question) :
    prompt = ChatPromptTemplate.from_messages([
        ("system", """너는 코딩 공부 커리큘럼의 한 차시 교안에 대한 질문을 받는 ai야.

교안은 다음과 같아: {curriculum_data}

유저의 질문에 대답해줘.

유저의 질문: {user_question}
    """),
        ("human", "답변해주세요."),
    ])
    llm = ChatOpenAI(
        temperature=0.5,
        model="gpt-4.1-mini",
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain
    

def create_chain(curriculum_data, age, language_level) : 
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""너는 코딩 공부 커리큘럼의 한 차시 배우는 내용을 기반으로 그 날의 교안을 생성해주는 AI야.
         
유저의 프로필은 다음과 같아:
- 나이: {age}
- 학습 수준(최하, 하, 중하, 중, 중상, 상, 최상 중 하나): {language_level}

커리큘럼의 한 차시의 정보는 다음과 같아: 
- 차시 제목: {curriculum_data['title']}
- 차시 내용: {curriculum_data['description']}

출력 형식은 아래와 같이 해줘: 

subtitle: 문단 제목
guide: 해당 내용에 대한 설명
example: 예시 코드
example_explanation: 예시 코드 설명
example_input: 예시 코드 실행 후 입력
example_output: 예시 코드 실행 후 출력
quiz: 퀴즈나 실습 문제

예: 차시 제목이 "파이썬 설치, print()"이고, 내용이 "파이썬을 설치하고 print()를 사용해봅시다."인 경우
{{{{
    {{{{
        "subtitle": "파이썬 설치",
        "guide": "파이썬을 설치해봅시다. 파이썬을 설치하려면 아래 단계를 따르세요. (어쩌구저쩌구)",
        "example": None,
        "example_explanation": None,
        "example_input": None,
        "example_output": None,
        "quiz": None,
    }}}},
    {{{{
        "subtitle": "파이썬 print() 사용",
        "guide": "파이썬에서 print()는 특정 내용을 출력하는 함수입니다. 사용법은 (어쩌구저쩌구)",
        "example": "print("Hello, World!")",
        "example_explanation": "print("Hello, World!")를 하면 print 안에 있는 Hello, World!가 출력됩니다.",
        "example_input": None,
        "example_output": "Hello, World!",
        "quiz": "print() 함수를 사용하여 `안녕하세요`를 출력해 보세요.",
    }}}}
}}}}

"""),
        ("human", "교안을 생성해주세요."),
    ])
    llm = ChatOpenAI(
        temperature=0.5,
        model="gpt-4.1-mini",
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain

st.session_state.chat_log = []

def main() : 
    if "user_id" not in st.session_state or not st.session_state.user_id:
        st.switch_page("pages/signin.py")
    
    if "selected_curriculum" not in st.session_state or not st.session_state.selected_curriculum:
        st.switch_page("pages/curriculum.py")
    
    if "selected_day" not in st.session_state or not st.session_state.selected_day:
        st.switch_page("pages/learn.py")
    
    curriculum_data = load_curriculum()[st.session_state.user_id][st.session_state.selected_curriculum][st.session_state.selected_day]
    st.title(f"{st.session_state.selected_curriculum} - {st.session_state.selected_day}")
    st.header(f"{curriculum_data['title']}")
    st.markdown(f"{curriculum_data['description']}")

    user_age = load_user_profile(st.session_state.user_id)["age"]
    user_language_level = load_user_profile(st.session_state.user_id)["language_level"]
    
    st.divider()

    chain = create_chain(curriculum_data, user_age, user_language_level)
    result = chain.invoke({"question": "교안을 생성해주세요."})
    
    try : 
        result_dict = json.loads(result)
    except : 
        st.error("교안 생성에 실패했습니다. 다시 시도해주세요.")
        return

    result_text = ""
    
    for section in result_dict:
        st.subheader(f"{section.get('subtitle', '')}")
        result_text += f"## {section.get('subtitle', '')}\n"
        st.markdown(f"**설명: **\n{section.get('guide', '')}")
        result_text += f"**설명: **\n{section.get('guide', '')}\n"
        if section.get('example'):
            st.markdown(f"**예시**: \n```python\n{section['example']}\n```")
            result_text += f"**예시**: \n```python\n{section['example']}\n```\n"
            st.markdown(f"**예시 설명**: \n{section.get('example_explanation', '')}")
            result_text += f"**예시 설명**: \n{section.get('example_explanation', '')}\n"
            if section.get('example_input'):
                st.markdown(f"**예시 입력**:\n{section['example_input']}")
                result_text += f"**예시 입력**:\n{section['example_input']}\n"
            if section.get('example_output'):
                st.markdown(f"**예시 출력**:\n{section['example_output']}")
                result_text += f"**예시 출력**:\n{section['example_output']}\n"
        if section.get('quiz'):
            st.markdown(f"**퀴즈**:\n{section['quiz']}")
            result_text += f"**퀴즈**:\n{section['quiz']}\n"
        st.divider()
    
    st.chat_message("assistant").markdown(f"교안이 생성되었습니다. 학습 중 궁금한 것이 있으시면 알려주세요!")

    st.session_state.chat_log.append({
        "role": "assistant",
        "content": f"{result_text}\n\n교안이 생성되었습니다. 학습 중 궁금한 것이 있으시면 알려주세요!"
    })

    temp = st.chat_input("아무 것이나 물어보세요...")

    if temp:
        st.chat_message("user").markdown(temp)
        st.session_state.chat_log.append({
            "role": "user",
            "content": temp
        })

        result = create_chat_chain(result_dict, temp).invoke({"curriculum_data": result_dict, "user_question": temp})
        st.chat_message("assistant").markdown(result)

        st.session_state.chat_log.append({
            "role": "assistant",
            "content": result
        })

main()