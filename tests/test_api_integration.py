import os
from unittest.mock import patch
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from maintainability.api.src import main, models

load_dotenv()
MAINTAINABILITY_API_KEY = os.getenv("MAINTAINABILITY_API_KEY")


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(main.app)
    yield client


def unique_email():
    return f"test+{uuid4()}@example.com"


def test_extract_metrics_with_valid_data(test_client):
    """Test /extract_metrics route with valid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    payload = {
        "project_name": "test_project",
        "filepath": "/test/path/testfile.py",
        "file_content": "print('hello world')\n" * 100,
        "session_id": "88888888-8888-8888-8888-888888888888",
    }
    response = test_client.post("/extract_metrics", headers=headers, json=payload)
    print(response.json())
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


@pytest.fixture(scope="module")
def generated_api_key(test_client):
    new_key = {"email": "fixture@test.com", "name": "fixturekey"}
    response = test_client.post("/generate_key", json=new_key)
    if response.status_code == 200 and "api_key" in response.json():
        return response.json()["api_key"]
    else:
        pytest.fail("Failed to generate API key for tests.")


def test_invalidate_api_key(test_client, generated_api_key):
    response = test_client.delete(f"/api_keys/{generated_api_key}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "API key deleted successfully"


def test_get_metrics_with_valid_project(test_client):
    user_email = "test"
    project_name = "test_project"
    params = {"user_email": user_email, "project_name": project_name}
    response = test_client.get("/get_metrics", params=params)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    for _, obj in response.json().items():
        assert "intuitive_design" in obj
        # ommitting other fields for brevity


def test_get_user_projects_with_valid_email(test_client):
    """Test /get_user_projects route with a valid email"""
    user_email = "test"
    params = {"user_email": user_email}
    response = test_client.get("/get_user_projects", params=params)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for project in response.json():
        assert "project_name" in project


def test_extract_metrics_with_default_response(test_client):
    """Test /extract_metrics route when get_maintainability_metrics fails"""

    mock_valid_model_response = models.MaintainabilityMetrics().model_dump()
    patch_path = "maintainability.api.src.routes_helper.get_maintainability_metrics"

    with patch(patch_path) as mock_get_metrics:
        mock_get_metrics.return_value = mock_valid_model_response
        headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
        payload = {
            "project_name": "test_project",
            "filepath": "/test/path/testfile.py",
            "file_content": "print('hello world')\n" * 100,
            "session_id": "88888888-8888-8888-8888-888888888888",
        }
        response = test_client.post("/extract_metrics", headers=headers, json=payload)

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        for metric, value in mock_valid_model_response.items():
            assert metric in response.json()
            assert response.json()[metric] == value
