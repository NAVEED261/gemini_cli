import streamlit as st
import random

def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-'])
    
    if operator == '+':
        question = f"{num1} + {num2}"
        answer = num1 + num2
    else:
        if num1 < num2:
            num1, num2 = num2, num1 # Swap to ensure num1 >= num2
        question = f"{num1} - {num2}"
        answer = num1 - num2
            
    return question, answer

st.set_page_config(page_title="Happy Math Puzzle Game", page_icon="🧠")

st.title("🧠 Happy Math Puzzle Game! 🧠")
st.write("Let's make your brain super strong with some fun math!")

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_num' not in st.session_state:
    st.session_state.question_num = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = None

num_questions = 5

def start_new_question():
    st.session_state.question_num += 1
    if st.session_state.question_num <= num_questions:
        st.session_state.current_question, st.session_state.correct_answer = generate_question()
    else:
        st.session_state.current_question = None

if st.session_state.current_question is None and st.session_state.question_num < num_questions:
    start_new_question()

if st.session_state.current_question:
    st.subheader(f"Question {st.session_state.question_num} of {num_questions}:")
    user_input = st.text_input(f"What is {st.session_state.current_question}? ", key=f"q_{st.session_state.question_num}")
    
    if st.button("Check Answer", key=f"btn_{st.session_state.question_num}"):
        try:
            user_answer = int(user_input)
            if user_answer == st.session_state.correct_answer:
                st.success("🎉 Yay! You got it right! You're a math superstar! 🎉")
                st.session_state.score += 1
            else:
                st.error(f"Aww, not quite! The correct answer was {st.session_state.correct_answer}. Keep trying, you'll get it next time! ")
        except ValueError:
            st.warning("Oops! That's not a number. Please enter a valid number.")
        
        # Move to next question after checking answer
        start_new_question()
        st.rerun()

else:
    st.subheader("--- Game Over ---")
    st.write(f"You answered {st.session_state.score} out of {num_questions} questions correctly!")
    
    if st.session_state.score == num_questions:
        st.balloons()
        st.success("🥳 Amazing! You are a Math Genius! Keep up the great work! 🥳")
    elif st.session_state.score >= num_questions / 2:
        st.info("🌟 Great job! You're doing wonderfully! Practice makes perfect! 🌟")
    else:
        st.warning("💡 You're learning so much! Every try makes you smarter! 💡")
        
    if st.button("Play Again?"):
        st.session_state.score = 0
        st.session_state.question_num = 0
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.experimental_rerun()