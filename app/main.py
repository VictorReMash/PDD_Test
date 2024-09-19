from tempfile import template

from fastapi import FastAPI, Depends, HTTPException  # Импортируем необходимые классы
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session, engine
from app import crud, models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from contextlib import asynccontextmanager
import os


# Определяем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))

# Шаблоны для отображения с использованием абсолютного пути
templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)


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


# Подключаем директорию для статических файлов с использованием абсолютного пути
images_dir = os.path.join(current_dir, "images")
app.mount("/images", StaticFiles(directory=images_dir), name="images")

static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# # Подключаем директорию для статических файлов
# app.mount("/images", StaticFiles(directory="app/images"), name="images")


# Получение зависимостей для сессии базы данных
async def get_db():
    async with async_session() as session:
        yield session


# Главная страница с кнопкой "Демо"
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Маршрут для получения вопроса по ID
# @app.get("/demo/{question_id}", response_class=HTMLResponse)
# async def get_question(
#     request: Request, question_id: int, db: AsyncSession = Depends(get_db)
# ):
#     question = await crud.get_question(db, question_id)
#     if not question:
#         raise HTTPException(status_code=404, detail="Вопрос не найден")
#
#     return templates.TemplateResponse(
#         "demo.html",
#         {
#             "question_text": question.question_text,
#             "request": request,
#             "image_url": question.image_url,
#             "chapter_id": question.chapter_id,
#         },
#     )
@app.get("/demo", response_class=HTMLResponse)
async def get_demo_page(request: Request, db: AsyncSession = Depends(get_db)):
    # Получаем первый вопрос из базы данных
    question = await crud.get_first_question(
        db
    )  # Делаем отдельную функцию для получения первого вопроса
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    return templates.TemplateResponse(
        "demo.html",
        {
            "request": request,
            "question_text": question.question_text,
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
