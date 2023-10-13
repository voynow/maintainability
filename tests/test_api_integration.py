import os
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from maintainability.api.src import main

load_dotenv()
MAINTAINABILITY_API_KEY = os.getenv("MAINTAINABILITY_API_KEY")


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(main.app)
    yield client


def unique_email():
    return f"test+{uuid4()}@example.com"


def get_test_content() -> str:
    return """
        from dataclasses import dataclass

        @dataclass
        class MaintainabilityMetrics:
            readability: int
            design_quality: int
            testability: int
            consistency: int
            debug_error_handling: int

        @dataclass
        class FileMetrics:
            file_size: int
            loc: int
            extension: str
            content: str

        @dataclass
        class CompositeMetrics:
            maintainability: MaintainabilityMetrics
            file_info: FileMetrics
            timestamp: str
            session_id: str"""


def generate_test_metrics():
    """Helper function to generate test metrics"""
    return {
        "/test/path/testfile.py": {
            "maintainability": {
                "readability": 3,
                "design_quality": 4,
                "testability": 3,
                "consistency": 7,
                "debug_error_handling": 1,
            },
            "file_info": {
                "file_size": 23,
                "loc": 1,
                "extension": "py",
                "content": get_test_content(),
            },
            "timestamp": "2023-09-27T00:00:00Z",
            "session_id": "88888888-8888-8888-8888-888888888888",
        }
    }


def test_submit_metrics_with_valid_data(test_client):
    """Test /submit_metrics route with valid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    response = test_client.post(
        "/submit_metrics", headers=headers, json=generate_test_metrics()
    )
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"


def test_submit_metrics_with_invalid_data(test_client):
    """Test /submit_metrics route with invalid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    response = test_client.post(
        "/submit_metrics", headers=headers, json={"invalid": "data"}
    )
    assert response.status_code == 422


def test_extract_metrics_with_valid_data(test_client):
    """Test /extract_metrics route with valid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    response = test_client.post(
        "/extract_metrics",
        headers=headers,
        json={"/test/path/testfile.py": "print('hello world')\n" * 100},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_extract_metrics_with_invalid_data(test_client):
    """Test /extract_metrics route with invalid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    response = test_client.post(
        "/extract_metrics", headers=headers, json={"invalid": -1}
    )
    assert response.status_code == 422


def test_health_route(test_client):
    """Test /health route"""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"


@pytest.fixture(scope="module")
def generated_api_key(test_client):
    new_key = {"email": "fixture@test.com", "name": "fixturekey"}
    response = test_client.post("/generate_key", json=new_key)
    if response.status_code == 200 and "api_key" in response.json():
        return response.json()["api_key"]
    else:
        pytest.fail("Failed to generate API key for tests.")


def test_successful_registration(test_client):
    user_data = {
        "email": unique_email(),
        "password": "test",
        "role": "user",
    }
    response = test_client.post("/register", json=user_data)
    assert response.status_code == 200
    assert "email" in response.json()


def test_successful_login(test_client):
    token_request = {"email": "login@test.com", "password": "test"}
    response = test_client.post("/token", json=token_request)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_unsuccessful_login(test_client):
    token_request = {"email": "unsuccessfullogin@test.com", "password": "wrongpassword"}
    response = test_client.post("/token", json=token_request)
    assert response.status_code == 401


def test_generate_api_key(test_client):
    new_key = {"email": "genapikey@test.com", "name": "testkey"}
    response = test_client.post("/generate_key", json=new_key)
    assert response.status_code == 200
    assert "api_key" in response.json()


def test_list_api_keys(test_client):
    response = test_client.get("/api_keys?email=listapikey@test.com")
    assert response.status_code == 200
    assert isinstance(response.json()["api_keys"], list)


def test_invalidate_api_key(test_client, generated_api_key):
    response = test_client.delete(f"/api_keys/{generated_api_key}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "API key deleted successfully"
