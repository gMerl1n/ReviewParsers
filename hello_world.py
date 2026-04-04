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
    return {"message": "Hello World"}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/hello/{name}")
async def hello_name(name: str) -> Dict[str, str]:
    return {"message": f"Hello, {name}!"}

@app.post("/hello/{name}")
async def create_name(name: str) -> Dict[str, str]:
    return {"message": f"{name} created"}
