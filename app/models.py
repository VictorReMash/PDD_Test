from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import VARCHAR

from app.database import Base


# Модель для таблицы "Chapters"
class Chapters(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(30), nullable=False)


# Модель для таблицы "questions"
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(255), nullable=False)  # Указана длина 255 символов
    image_url = Column(String(255), nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)


# Модель для таблицы "answers"
class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String(255), nullable=False)
    correct_answer = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
