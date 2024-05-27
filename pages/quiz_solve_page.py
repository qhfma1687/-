#quiz_solve_page.py

import streamlit as st
from langchain_core.pydantic_v1 import BaseModel, Field
from PyPDF2 import PdfReader
import json

def store_answers(user_answers, correct_answers):
    st.session_state['user_answers'] = user_answers
    st.session_state['correct_answers'] = correct_answers

def quiz_solve_page():
    if st.session_state.selected_type == '다중 선택 (객관식)':
        placeholder = st.empty()
        if 'number' not in st.session_state:
            st.session_state.number = 0
        if 'user_selected_answers' not in st.session_state:
            st.session_state.user_selected_answers = []  # 사용자 선택 답변을 저장할 배열 초기화

        for j, question in enumerate(st.session_state.quizs):
            if st.session_state.number == j:
                with placeholder.container():
                    res = json.loads(question["answer"])
                    st.header(f"질문 {j+1}")
                    st.write(f"{question}")
                    options = [res.get('options1'), res.get('options2'), res.get('options3'), res.get('options4')]
                    
                    for index, option in enumerate(options):
                        if st.button(f"{index+1}. {option}", key=f"{j}_{index}"):
                            st.session_state.user_selected_answers.append(option)  # 선택한 답변을 배열에 추가
                            st.session_state.number += 1  # 다음 문제로 이동

                            if st.session_state.user_selected_answers.append == st.session_state.quizs[j]['answer']:
                                total_score += 1
                            # if st.session_state.number == len(st.session_state.quizs):
                            #     if st.button('퀴즈 채점'):
                            #         st.session_state['total_score'] = st.session_state.number  # 점수를 세션 상태에 저장
                            #         st.switch_page("pages/quiz_grading_page.py")
                                # st.session_state.number = 0  # 모든 문제를 다 풀면 처음으로 돌아감
                                # st.experimental_rerun()  # 페이지 새로고침
        
        if st.session_state.number == st.session_state.selected_num:
            st.write("\n")
            if st.button('퀴즈 채점'):
                st.session_state['total_score'] = st.session_state.number  # 점수를 세션 상태에 저장
                st.switch_page("pages/quiz_grading_page.py")

        # 사용자가 선택한 답변 출력
        if st.session_state.user_selected_answers:
            st.write("사용자가 선택한 답변:")
            for answer in st.session_state.user_selected_answers:
                st.write(answer)

    elif st.session_state.selected_type == "주관식":
        st.write("\n")
        st.session_state.canswer = st.text_input(f"질문{j + 1}에 대한 답변 입력", key=f"{j}1")
        st.session_state.uanswer = st.session_state.canswer

    elif st.session_state.selected_type == 'OX 퀴즈':
        if st.button(f"1.{res['options1']}", key=f"{j}1"):
            st.session_state.canswer = res['options1']
            st.session_state.uanswer = res['options1']
            st.session_state.number += 1  # 다음 문제로 이동
        if st.button(f"2.{res['options2']}", key=f"{j}2"):
            st.session_state.canswer = res['options2']
            st.session_state.uanswer = res['options2']
    st.write("-----------------------------------------")
    
if __name__ == "__main__":
    quiz_solve_page()




