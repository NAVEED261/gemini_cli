import random

def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-'])
    
    if operator == '+':
        question = f"What is {num1} + {num2}? "
        answer = num1 + num2
    else:
        # Ensure result is not negative for simpler kids' math
        if num1 < num2:
            num1, num2 = num2, num1 # Swap to ensure num1 >= num2
        question = f"What is {num1} - {num2}? "
        answer = num1 - num2
            
    return question, answer

def play_game():
    print("Welcome to the Happy Math Puzzle Game!")
    print("Let's make your brain super strong with some fun math!")
    
    score = 0
    num_questions = 5
    
    for i in range(num_questions):
        question, correct_answer = generate_question()
        print(f"\nQuestion {i + 1}:")
        
        try:
            user_answer = int(input(question))
        except ValueError:
            print("Oops! That's not a number. Try again!")
            user_answer = -1 # Assign a wrong answer
            
        if user_answer == correct_answer:
            print("Yay! You got it right! You're a math superstar!")
            score += 1
        else:
            print(f"Aww, not quite! The correct answer was {correct_answer}. Keep trying, you'll get it next time!")
            
    print("\n--- Game Over ---")
    print(f"You answered {score} out of {num_questions} questions correctly!")
    
    if score == num_questions:
        print("Amazing! You are a Math Genius! Keep up the great work!")
    elif score >= num_questions / 2:
        print("Great job! You're doing wonderfully! Practice makes perfect!")
    else:
        print("You're learning so much! Every try makes you smarter!")

if __name__ == "__main__":
    play_game()
