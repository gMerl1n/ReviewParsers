import pytest
from fastapi.testclient import TestClient
from main import app  # Предполагается, что ваш файл называется main.py

client = TestClient(app)


class TestHealthEndpoint:
    """Тесты для эндпоинта /health"""

    def test_health_returns_ok(self):
        """Проверяет, что ручка /health возвращает status: ok"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_response_structure(self):
        """Проверяет структуру ответа /health"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert isinstance(data["status"], str)

    def test_health_method_not_allowed(self):
        """Проверяет, что POST запрос к /health возвращает 405"""
        response = client.post("/health")
        assert response.status_code == 405


class TestParseEndpoint:
    """Тесты для эндпоинта /parse"""

    def test_parse_returns_parser_starting(self):
        """Проверяет, что ручка /parse возвращает корректное сообщение"""
        response = client.get("/parse")
        assert response.status_code == 200
        assert response.json() == {"message": "parser starting"}

    def test_parse_response_structure(self):
        """Проверяет структуру ответа /parse"""
        response = client.get("/parse")
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)

    def test_parse_method_not_allowed(self):
        """Проверяет, что POST запрос к /parse возвращает 405"""
        response = client.post("/parse")
        assert response.status_code == 405


class TestReviewsEndpoint:
    """Тесты для эндпоинта /reviews"""

    def test_reviews_returns_list_of_dicts(self):
        """Проверяет, что ручка /reviews возвращает список отзывов"""
        response = client.get("/reviews")
        assert response.status_code == 200

        data = response.json()
        assert "reviews" in data
        assert isinstance(data["reviews"], list)

    def test_reviews_contains_expected_structure(self):
        """Проверяет структуру каждого отзыва"""
        response = client.get("/reviews")
        data = response.json()

        for review in data["reviews"]:
            assert isinstance(review, dict)
            # Проверяем, что в каждом словаре есть ключи "1" и "2"
            assert "1" in review
            assert "2" in review
            assert review["1"] == "review-1"
            assert review["2"] == "review-2"

    def test_reviews_returns_exactly_two_reviews(self):
        """Проверяет, что возвращается ровно два отзыва"""
        response = client.get("/reviews")
        data = response.json()
        assert len(data["reviews"]) == 2

    def test_reviews_method_not_allowed(self):
        """Проверяет, что POST запрос к /reviews возвращает 405"""
        response = client.post("/reviews")
        assert response.status_code == 405


class TestNotFound:
    """Тесты для несуществующих эндпоинтов"""

    def test_not_found_endpoint(self):
        """Проверяет, что несуществующий эндпоинт возвращает 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_not_found_method(self):
        """Проверяет, что неразрешённый метод возвращает 405"""
        response = client.put("/health")
        assert response.status_code == 405
