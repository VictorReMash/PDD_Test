from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+aiomysql://usertest:4MDI8c81@localhost:3306/test_form"

# Базовый класс для моделей
Base = declarative_base()

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
