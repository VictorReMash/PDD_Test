async function fetchQuestion(questionId) {
    const response = await fetch(`/api/question/${questionId}`);
    const data = await response.json();

    // Проверяем, есть ли ошибка
    if (data.error) {
        alert(data.error);
        return;
    }

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

// Добавляем обработчики событий на кнопки
document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll('button[data-question-id]');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const questionId = button.getAttribute('data-question-id');
            fetchQuestion(questionId);
        });
    });
});
