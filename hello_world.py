from fastapi import FastAPI
from typing import Dict

# Создание экземпляра приложения
app = FastAPI(
    title="Hello World API",
    description="Простой FastAPI сервер с ручкой hello world",
    version="1.0.0"
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Корневой эндпоинт"""
    return {"message": "Hello World"}


@app.get("/health")
async def health() -> Dict[str, str]:
    """Эндпоинт для проверки здоровья сервера"""
    return {"status": "ok"}


@app.get("/hello/{name}")
async def hello_name(name: str) -> Dict[str, str]:
    """Эндпоинт с параметром в пути"""
    return {"message": f"Hello, {name}!"}