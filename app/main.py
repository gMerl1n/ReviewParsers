from fastapi import FastAPI
from typing import Dict, List

# Создание экземпляра приложения
app = FastAPI(
    title=" API",
    version="1.0.0",
)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/parse")
async def parse() -> Dict[str, str]:
    return {"message": "parser starting"}

@app.get("/reviews")
async def parse() -> Dict[str, List[dict]]:
    return {
        "reviews": [
            {"1": "review-1"},
            {"2": "review-2"},
        ]
    }
