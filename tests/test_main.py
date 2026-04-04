import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRoot:
    """Тесты для корневого эндпоинта /"""

    def test_root_returns_hello_world(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_root_content_type_is_json(self):
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestHealth:
    """Тесты для эндпоинта здоровья /health"""

    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_check_always_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.status_code != 500
        assert response.status_code != 404


class TestHelloName:
    """Тесты для эндпоинтов /hello/{name}"""

    def test_hello_name_returns_greeting(self):
        response = client.get("/hello/Peter")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, Peter!"}

    def test_hello_name_with_different_names(self):
        names = ["John", "Alice", "Max", "Елена", "123"]
        for name in names:
            response = client.get(f"/hello/{name}")
            assert response.status_code == 200
            assert response.json() == {"message": f"Hello, {name}!"}

    def test_hello_name_with_url_encoded_name(self):
        response = client.get("/hello/John%20Doe")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, John Doe!"}

    def test_hello_name_with_empty_name(self):
        response = client.get("/hello/")
        assert response.status_code == 404

    def test_hello_name_with_special_characters(self):
        response = client.get("/hello/@#$%")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_post_hello_name_returns_created_message(self):
        response = client.post("/hello/John")
        assert response.status_code == 200
        assert response.json() == {"message": "John created"}

    def test_post_hello_name_with_different_names(self):
        names = ["Alice", "Bob", "Charlie"]
        for name in names:
            response = client.post(f"/hello/{name}")
            assert response.status_code == 200
            assert response.json() == {"message": f"{name} created"}

    def test_post_hello_name_method_not_allowed(self):
        response = client.put("/hello/John")
        assert response.status_code == 405

    def test_get_hello_name_method_not_allowed_for_post_only(self):
        response = client.put("/hello/John")
        assert response.status_code == 405
        response = client.delete("/hello/John")
        assert response.status_code == 405


class TestNames:
    """Тесты для эндпоинта /names"""

    def test_get_names_returns_dict(self):
        response = client.post("/names")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_names_returns_expected_data(self):
        response = client.post("/names")
        assert response.status_code == 200
        assert response.json() == {"1": "John", "2": "Ivan"}

    def test_get_names_returns_integer_keys(self):
        response = client.post("/names")
        data = response.json()
        keys = [int(k) for k in data.keys()]
        assert keys == [1, 2]

    def test_get_names_returns_string_values(self):
        response = client.post("/names")
        data = response.json()
        assert isinstance(data["1"], str)
        assert isinstance(data["2"], str)

    def test_get_names_method_not_allowed(self):
        response = client.get("/names")
        assert response.status_code == 405

    def test_get_names_always_returns_same_data(self):
        response1 = client.post("/names")
        response2 = client.post("/names")
        assert response1.json() == response2.json()


class TestNotFound:
    """Тесты для несуществующих эндпоинтов"""

    def test_not_found_endpoint(self):
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_not_found_method(self):
        response = client.delete("/")
        assert response.status_code == 405


class TestResponseStructure:
    """Тесты структуры ответов"""

    def test_all_responses_are_json(self):
        endpoints = ["/", "/health", "/hello/John"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.headers["content-type"] == "application/json"

    def test_all_responses_have_message_or_status(self):
        response_root = client.get("/")
        assert "message" in response_root.json()

        response_health = client.get("/health")
        assert "status" in response_health.json()

        response_hello = client.get("/hello/John")
        assert "message" in response_hello.json()
