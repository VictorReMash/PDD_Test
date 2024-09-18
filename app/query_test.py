import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.database import DATABASE_URL
from app.models import Answers
from models import Question  # Предположим, что модель Question уже определена

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание сессии
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Асинхронная функция для получения вопроса
async def get_question(db: AsyncSession, question_id: int):
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()


# Асинхронная функция для получения ответов на вопрос
async def get_answer(db: AsyncSession, question_id: int):
    result = await db.execute(select(Answers).where(Answers.question_id == question_id))
    return result.scalar_one_or_none()


# Тестовая функция с параметром question_id
async def test_get_question(question_id: int):
    # Создаём сессию для работы с базой данных
    async with SessionLocal() as session:
        question = await get_question(session, question_id)

        # Выводим результат
        if question:
            print(f"Question ID: {question.id}, Text: {question.question_text}")
        else:
            print("Question not found.")


# Запуск в блоке if __name__ == '__main__'
if __name__ == "__main__":
    # Передача question_id в качестве аргумента
    question_id = 1  # Укажи тестовый ID вопроса
    asyncio.run(test_get_question(question_id))
