import streamlit as st

st.session_state.user_id = None
st.success("로그아웃 성공.")
st.switch_page("pages/signin.py")