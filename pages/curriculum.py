import streamlit as st
import json
from pathlib import Path
from function import *

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
curriculum_path = DATA_DIR / "curriculums.json"

def display_curriculum_list(user_id: str):
    curriculums = load_curriculum()
        
    st.subheader("커리큘럼 목록")

    if st.button("커리큘럼 생성") : 
        st.switch_page("pages/new_curriculum.py")

    if not curriculums.get(user_id):
        st.warning("커리큘럼이 없습니다.")
        return
    
    # 편집 모달 상태 변수 초기화
    if "edit_modal_open" not in st.session_state:
        st.session_state.edit_modal_open = False
    if "editing_curriculum_id" not in st.session_state:
        st.session_state.editing_curriculum_id = None
    if "new_curriculum_name" not in st.session_state:
        st.session_state.new_curriculum_name = ""

    # 현재 유저 아이디 보관 (dialog 내부에서 사용)
    st.session_state.current_user_id = user_id

    # 다이얼로그 정의
    @st.dialog("커리큘럼 이름 수정")
    def curriculum_edit_dialog():
        st.text_input(
            "새 커리큘럼 이름",
            key="new_curriculum_name",
        )
        if st.button("수정", type="primary", key="confirm_edit"):
            new_name = (st.session_state.get("new_curriculum_name") or "").strip()
            old_name = st.session_state.get("editing_curriculum_id")
            user_id_inner = st.session_state.get("current_user_id")
            curriculums_inner = load_curriculum()
            user_curriculums = curriculums_inner.get(user_id_inner, {})
            if not new_name:
                st.warning("새 커리큘럼 이름을 입력하세요.")
            elif new_name == old_name:
                st.session_state.edit_modal_open = False
                st.session_state.editing_curriculum_id = None
                try:
                    st.rerun()
                except Exception:
                    st.experimental_rerun()
            else:
                if new_name in user_curriculums:
                    st.error("같은 이름의 커리큘럼이 이미 있습니다. 다른 이름을 입력하세요.")
                else:
                    curriculums_inner[user_id_inner][new_name] = curriculums_inner[user_id_inner][old_name]
                    del curriculums_inner[user_id_inner][old_name]
                    save_curriculums(curriculums_inner)
                    st.session_state.edit_modal_open = False
                    st.session_state.editing_curriculum_id = None
                    try:
                        st.rerun()
                    except Exception:
                        st.experimental_rerun()

    # 각 커리큘럼을 카드 형태로 표시 (역순)
    for idx, (curriculum_id, curriculum_data) in enumerate(reversed(list(curriculums[user_id].items()))):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{curriculum_id}**")
            
            with col2:
                if st.button("선택", key=f"select_{idx}"):
                    st.session_state.selected_curriculum = curriculum_id
                    st.switch_page("pages/learn.py")
                # 선택 버튼 아래 커리큘럼 수정 버튼
                if st.button("커리큘럼 수정", key=f"edit_{idx}"):
                    st.session_state.edit_modal_open = True
                    st.session_state.editing_curriculum_id = curriculum_id
                    st.session_state.new_curriculum_name = curriculum_id
            
            st.divider()

    # 커리큘럼 이름 수정 모달 띄우기
    if st.session_state.edit_modal_open:
        curriculum_edit_dialog()

def main() : 
    if "user_id" not in st.session_state or not st.session_state.user_id:
        st.switch_page("pages/signin.py")
    
    display_curriculum_list(st.session_state.user_id)

main()