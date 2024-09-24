from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Question
from app.utils import demolist


# Получение первого вопроса из базы данных
async def get_first_question(db: AsyncSession):
    result = await db.execute(select(Question).order_by(Question.id.asc()).limit(1))
    return result.scalar_one_or_none()


# Получение всех вопросов из базы данных
async def get_all_questions(db: AsyncSession):
    result = await db.execute(select(Question).filter(Question.id.in_(demolist)))
    return result.scalars().all()


# Получение вопроса по ID
async def get_question(db: AsyncSession, question_id: int):
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()


# Добавление нового вопроса
async def create_question(
    db: AsyncSession, question_text: str, chapter_id: int, image_url: str = None
):
    new_question = Question(
        question_text=question_text, chapter_id=chapter_id, image_url=image_url
    )
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question
