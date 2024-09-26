let currentQuestionIndex = 0; // Индекс текущего вопроса
const buttons = document.querySelectorAll('button[data-question-id]'); // Получаем все кнопки
const totalQuestions = buttons.length; // Общее количество вопросов
let answeredQuestions = new Set(); // Множество отвеченных вопросов

// Функция для получения вопроса по ID
async function fetchQuestion(questionId) {
    const response = await fetch(`/api/question/${questionId}`);
    const data = await response.json();

    // Проверяем, есть ли ошибка
    if (data.error) {
        alert(data.error);
        return;
    }

    // Сброс состояния радиокнопок
    const optionInputs = document.querySelectorAll('input[name="chapter_id"]');
    optionInputs.forEach(input => {
        input.checked = false; // Сбрасываем все радиокнопки
    });

    // Обновляем содержимое вопроса на странице
    const imageElement = document.querySelector('.test__image');
    const questionElement = document.querySelector('.test__question');
    const optionInput = document.querySelector('.test__input');
    const optionLabel = document.querySelector('.test__label');

    imageElement.src = data.image_url;  // Устанавливаем новый URL изображения
    questionElement.textContent = data.question_text;  // Устанавливаем текст вопроса
    optionInput.value = data.chapter_id;  // Устанавливаем значение радиокнопки
    optionLabel.textContent = data.chapter_id;  // Устанавливаем текст метки радиокнопки
}

// Функция для получения следующего неотвеченного вопроса
function getNextUnansweredQuestion() {
    for (let i = currentQuestionIndex + 1; i < totalQuestions; i++) {
        if (!answeredQuestions.has(i)) {
            return i;
        }
    }
    return -1; // Если все вопросы отвечены
}

// Обработчик события для кнопки "Ответить"
async function handleAnswerSubmit(event) {
    event.preventDefault(); // Предотвращаем отправку формы

    const answerValue = document.querySelector('input[name="chapter_id"]:checked')?.value;

    if (!answerValue) {
        alert("Пожалуйста, выберите вариант ответа.");
        return;
    }

    // Добавляем текущий вопрос в множество отвеченных
    answeredQuestions.add(currentQuestionIndex);

    // Переходим к следующему неотвеченному вопросу
    const nextQuestionIndex = getNextUnansweredQuestion();

    if (nextQuestionIndex !== -1) {
        currentQuestionIndex = nextQuestionIndex; // Обновляем индекс следующего вопроса
        const nextButton = buttons[currentQuestionIndex]; // Получаем следующую кнопку
        const nextQuestionId = nextButton.getAttribute('data-question-id'); // Получаем ID следующего вопроса
        fetchQuestion(nextQuestionId); // Загружаем следующий вопрос
    } else {
        alert("Тест завершен!");
        // Логика завершения теста
    }
}

// Добавляем обработчики событий на кнопки
document.addEventListener("DOMContentLoaded", () => {
    buttons.forEach((button, index) => {
        button.addEventListener('click', () => {
            const questionId = button.getAttribute('data-question-id');
            fetchQuestion(questionId);

            // Обновляем currentQuestionIndex в зависимости от выбранной кнопки
            currentQuestionIndex = index;
        });
    });

    // Добавляем обработчик события для формы
    const form = document.querySelector('.test__form');
    form.addEventListener('submit', handleAnswerSubmit);
});
