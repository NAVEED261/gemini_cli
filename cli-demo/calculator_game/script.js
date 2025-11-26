const problemElement = document.getElementById('problem');
const answerInput = document.getElementById('answer-input');
const submitBtn = document.getElementById('submit-btn');
const scoreElement = document.getElementById('score');
const timeElement = document.getElementById('time');
const feedbackElement = document.getElementById('feedback');
const startBtn = document.getElementById('start-btn');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreElement = document.getElementById('final-score');
const restartBtn = document.getElementById('restart-btn');
const gameContainer = document.querySelector('.game-container');

let score = 0;
let timeLeft = 60;
let timer;
let currentProblem;
let gameActive = false;

function generateProblem() {
    const num1 = Math.floor(Math.random() * 10) + 1; // Numbers 1-10
    const num2 = Math.floor(Math.random() * 10) + 1;
    const operators = ['+', '-', '*', '/'];
    const operator = operators[Math.floor(Math.random() * operators.length)];
    let problemString;
    let correctAnswer;

    // Ensure division results in whole numbers for simplicity
    if (operator === '/') {
        // Make sure num1 is a multiple of num2 and num2 is not 0
        let tempNum1 = num1 * num2; // Ensure divisibility
        problemString = `${tempNum1} ${operator} ${num2}`;
        correctAnswer = tempNum1 / num2;
    } else {
        problemString = `${num1} ${operator} ${num2}`;
        switch (operator) {
            case '+':
                correctAnswer = num1 + num2;
                break;
            case '-':
                correctAnswer = num1 - num2;
                break;
            case '*':
                correctAnswer = num1 * num2;
                break;
        }
    }

    problemElement.textContent = problemString;
    return correctAnswer;
}

function startGame() {
    gameActive = true;
    score = 0;
    timeLeft = 60;
    scoreElement.textContent = score;
    timeElement.textContent = timeLeft;
    feedbackElement.textContent = '';
    answerInput.value = '';
    gameOverScreen.classList.remove('active');
    gameContainer.classList.add('game-active');
    answerInput.focus();

    currentProblem = generateProblem();
    timer = setInterval(() => {
        timeLeft--;
        timeElement.textContent = timeLeft;
        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function endGame() {
    gameActive = false;
    clearInterval(timer);
    finalScoreElement.textContent = score;
    gameOverScreen.classList.add('active');
    gameContainer.classList.remove('game-active');
}

function checkAnswer() {
    if (!gameActive) return;

    const userAnswer = parseInt(answerInput.value);
    if (isNaN(userAnswer)) {
        feedbackElement.textContent = 'Please enter a number!';
        feedbackElement.className = 'feedback incorrect';
        return;
    }

    if (userAnswer === currentProblem) {
        score++;
        scoreElement.textContent = score;
        feedbackElement.textContent = 'Correct!';
        feedbackElement.className = 'feedback correct';
    } else {
        feedbackElement.textContent = `Incorrect! It was ${currentProblem}`;
        feedbackElement.className = 'feedback incorrect';
    }

    answerInput.value = '';
    currentProblem = generateProblem();
    answerInput.focus();
}

submitBtn.addEventListener('click', checkAnswer);
answerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        checkAnswer();
    }
});
startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', startGame);

// Initial state setup
gameContainer.classList.remove('game-active');
