from fastapi import FastAPI, Depends, HTTPException  # Импортируем необходимые классы
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session, engine
from app import crud, models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from contextlib import asynccontextmanager

# Шаблоны для отображения
templates = Jinja2Templates(directory="app/templates")


# Новый способ обработки событий жизненного цикла через lifespan
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Инициализация базы данных при старте
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    # Вход в приложение
    yield

    # Выход из приложения (если нужно что-то закрыть или очистить)
    await engine.dispose()


# Инициализируем приложение с lifespan
app = FastAPI(lifespan=lifespan)

# Подключаем директорию для статических файлов
app.mount("/images", StaticFiles(directory="app/images"), name="images")


# Получение зависимостей для сессии базы данных
async def get_db():
    async with async_session() as session:
        yield session


# Маршрут для получения вопроса по ID
@app.get("/question/{question_id}", response_class=HTMLResponse)
async def get_question(
    request: Request, question_id: int, db: AsyncSession = Depends(get_db)
):
    question = await crud.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    return templates.TemplateResponse(
        "index.html",
        {
            "question_text": question.question_text,
            "request": request,
            "image_url": question.image_url,
            "chapter_id": question.chapter_id,
        },
    )


# Добавление нового вопроса (для примера)
@app.post("/question/")
async def create_question(
    question_text: str,
    chapter_id: int,
    image_url: str = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_question(db, question_text, chapter_id, image_url)


import os


@app.get("/images")
async def list_images():
    files = os.listdir("app/images")
    return {"images": files}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
