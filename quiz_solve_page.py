#quiz_solve_page.py

import streamlit as st
from langchain_core.pydantic_v1 import BaseModel, Field
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
import io

class CreateQuizoub(BaseModel):
    quiz: str = Field(description="만들어진 문제")
    options1: str = Field(description="만들어진 문제의 첫 번째 보기")
    options2: str = Field(description="만들어진 문제의 두 번째 보기")
    options3: str = Field(description="만들어진 문제의 세 번째 보기")
    options4: str = Field(description="만들어진 문제의 네 번째 보기")
    correct_answer: str = Field(description="options1, options2, options3, options4중 하나")


class CreateQuizsub(BaseModel):
    quiz: str = Field(description="만들어진 문제")
    correct_answer: str = Field(description="만들어진 문제의 답")


class CreateQuizTF(BaseModel):
    quiz: str = Field(description="만들어진 문제")
    options1: str = Field(description="만들어진 문제의 참 또는 거짓인 보기")
    options2: str = Field(description="만들어진 문제의 참 또는 거짓인 보기")
    correct_answer: str = Field(description="만들어진 보기중 하나")

# 퀴즈 채점 함수
@st.experimental_fragment
def grade_quiz_answers(user_answers, quiz_answers):
    graded_answers = []
    for user_answer, quiz_answer in zip(user_answers, quiz_answers):
        if user_answer.lower() == quiz_answer.lower():
            graded_answers.append("정답")
        else:
            graded_answers.append("오답")
    st.session_state['ganswer'] = graded_answers
    return graded_answers

# 파일 처리 함수
@st.experimental_fragment
def process_file(uploaded_file):
    if uploaded_file is None:
        st.warning("파일을 업로드하세요.")
        return None

    # 업로드된 파일 처리
    if uploaded_file.type == "text/plain":
        text_content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type.startswith("image/"):
        image = Image.open(uploaded_file)
        text_content = pytesseract.image_to_string(image)
    elif uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
    else:
        st.error("지원하지 않는 파일 형식입니다.")
        return None

    return text_content

# 퀴즈 생성 함수
@st.experimental_fragment
def generate_quiz(quiz_type, text_content):
    response = CreateQuizoub
    response.quiz = '어댑터패턴이나 퍼사드패턴은 무엇을 위해 사용되는가?'
    response.options1 = '인터페이스 호환성 때문에 같이 쓸 수 없는 클래스들을 연결해서 사용할 수 있게 함'
    response.options2 = '복잡한 서브시스템을 더 쉽게 사용할 수 있게 해줌'
    response.options3 = '객체의 인터페이스를 다른 인터페이스로 변환할 때 사용함'
    response.options4 = '상속을 사용하여 서브클래스에 대해서 어댑터 역할을 수행함'
    response.correct_answer = '인터페이스 호환성 때문에 같이 쓸 수 없는 클래스들을 연결해서 사용할 수 있게 함'
    quiz_questions = response

    return quiz_questions

@st.experimental_fragment
def grade_quiz_answer(user_answer, quiz_answer):
    if user_answer.lower() == quiz_answer.lower():
        grade = "정답"
    else:
        grade = "오답"
    return grade


def quiz_solve_page():
    placeholder = st.empty()
    if 'number' not in st.session_state:
        st.session_state.number = 0
    for j, question in enumerate(st.session_state.quizs):
        if st.session_state.number == j:
            with placeholder.container():
                st.header("생성된 퀴즈")
                st.write(st.session_state.selected_page)
                st.write(st.session_state.number)
                st.write(f"{question}")
                st.write(f"{j+1}.{question.answer.quiz}")
                st.write(f"{j+1}.{question.quiz}")
                st.write("\n")
                if st.session_state.selected_type == "주관식":
                    st.write("\n")
                    st.session_state.canswer = st.text_input(f"질문{j + 1}에 대한 답변 입력", key=f"{j}1")
                elif st.session_state.selected_type == '다중 선택 (객관식)':
                    if st.button(f"1.{question.answer.options1}", key=f"{j}1"):
                    if st.button(f"1.{question.options1}", key=f"{j}1"):
                        st.session_state.canswer = "options1"
                    if st.button(f"2.{question.answer.options2}", key=f"{j}2"):
                    if st.button(f"2.{question.options2}", key=f"{j}2"):
                        st.session_state.canswer = "options2"
                    if st.button(f"3.{question.answer.options3}", key=f"{j}3"):
                    if st.button(f"3.{question.options3}", key=f"{j}3"):
                        st.session_state.canswer = "options3"
                    if st.button(f"4.{question.answer.options4}", key=f"{j}4"):
                    if st.button(f"4.{question.options4}", key=f"{j}4"):
                        st.session_state.canswer = "options4"
                elif st.session_state.selected_type == 'OX 퀴즈':
                    if st.button(f"1.{question.answer.options1}", key=f"{j}1"):
                        st.session_state.canswer = question.answer.options1
                    if st.button(f"2.{question.answer.options2}", key=f"{j}2"):
                        st.session_state.canswer = question.answer.options2
                    if st.button(f"1.{question.options1}", key=f"{j}1"):
                        st.session_state.canswer = question.options1
                    if st.button(f"2.{question.options2}", key=f"{j}2"):
                        st.session_state.canswer = question.options2
                st.write("-----------------------------------------")
                st.write("\n")
                if st.button("next", key= f"next{j}"):
                    if question.correct_answer == st.session_state.canswer:
                        st.write("Correct")
                        st.session_state.number += 1
                    else:
                        st.write("Wrong")

        j += 1
    if st.session_state.number == st.session_state.selected_num:
        st.session_state.selected_page = "퀴즈 생성"
        st.rerun()
