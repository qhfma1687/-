import streamlit as st
import quiz_creation_page
import quiz_solve_page
import quiz_grading_page
import sign

def main():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ["퀴즈 생성", "퀴즈 풀이", "퀴즈 채점", "로그인"])

    if selected_page == "퀴즈 생성":
        quiz_creation_page.quiz_creation_page()
    elif selected_page == "퀴즈 풀이":
        quiz_solve_page.quiz_solve_page()
    elif selected_page == "퀴즈 채점":
        quiz_grading_page.quiz_grading_page()
    elif selected_page == "로그인":
        sign.sign()

if __name__ == "__main__":
    main()
