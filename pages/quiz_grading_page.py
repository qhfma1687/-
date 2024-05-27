#quiz_grading_page.py
import streamlit as st
from langchain_openai import ChatOpenAI

def grade_quiz_answers(user_answers, correct_answers):
    graded_answers = []
    for user_answer, correct_answer in zip(user_answers, correct_answers):
        if user_answer == correct_answer:
            graded_answers.append('정답')
        else:
            graded_answers.append('오답')
    return graded_answers

def get_openai_explanation(question, correct_answer):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    prompt = f"문제: {question}\n정답: {correct_answer}\n이 문제의 해설을 제공해주세요."
    response = llm(prompt)
    return response

def quiz_grading_page():
    user_answers = st.session_state.get('user_selected_answers', [])
    correct_answers = st.session_state.get('correct_answers', [])
    questions = st.session_state.get('quiz_questions', [])
    graded_answers = grade_quiz_answers(user_answers, correct_answers)

    st.title("퀴즈 채점 결과")
    total_score = 0

    for i, (question, user_answer, correct_answer, result) in enumerate(zip(questions, user_answers, correct_answers, graded_answers), start=1):
        st.subheader(f"문제 {i}")
        st.write(f"문제: {question}")
        st.write(f"사용자 답변: {user_answer}")
        st.write(f"정답: {correct_answer}")
        if result == "정답":
            st.success("정답입니다!", key=f"result_success_{i}")
            total_score += 1
        else:
            st.error("오답입니다.", key=f"result_error_{i}")
        
        explanation = get_openai_explanation(question, correct_answer)
        st.write(f"해설: {explanation}")

    st.write(f"당신의 점수는 {total_score}점 입니다.")

    if st.button("퀴즈 생성 페이지로 이동", key="go_to_creation_page"):
        st.session_state["page"] = "quiz_creation_page"

if __name__ == "__main__":
    quiz_grading_page()
