import os
from datetime import datetime
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

os.environ["SKIP_AUTH_MIDDLEWARE"] = "True"
from maintainability.api.src import main, io_operations, models

load_dotenv()
MAINTAINABILITY_API_KEY = os.getenv("MAINTAINABILITY_API_KEY")


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(main.app)
    yield client


def unique_email():
    return f"test+{uuid4()}@example.com"


def test_health_route(test_client):
    """Test /health route"""
    response = test_client.get("/health")
    assert response.status_code == 200, response.text
    assert "status" in response.json(), response.text
    assert response.json()["status"] == "ok", response.text


def test_extract_metrics_with_valid_data(test_client):
    """Test /extract_metrics route with valid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    payload = {
        "file_id": "88888888-8888-8888-8888-888888888888",
        "session_id": "88888888-8888-8888-8888-888888888888",
        "file_path": "/test/path/testfile.py",
        "content": "print('hello world')\n" * 100,
        "metric_name": "adaptive_resilience",
    }
    response = test_client.post("/extract_metrics", headers=headers, json=payload)
    assert response.status_code == 200, response.text
    assert "file_id" in response.json()
    assert response.json()["file_id"] == payload["file_id"], response.text


def test_extract_metrics_with_invalid_data(test_client):
    """Test /extract_metrics route with invalid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    response = test_client.post(
        "/extract_metrics", headers=headers, json={"invalid": -1}
    )
    assert response.status_code == 422, response.text


def test_insert_file(test_client):
    """Test /insert_file route with valid data"""
    headers = {"X-API-KEY": MAINTAINABILITY_API_KEY}
    file_id = str(uuid4())
    session_id = str(uuid4())
    timestamp = datetime.now().isoformat()
    payload = {
        "file_id": file_id,
        "file_path": "/test/path/testfile.py",
        "content": "print('hello world')\n" * 100,
        "user_email": "test",
        "project_name": "test_project",
        "session_id": session_id,
        "file_size": 100,
        "loc": 100,
        "extension": "",
        "timestamp": timestamp,
    }
    response = test_client.post("/insert_file", headers=headers, json=payload)
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), dict), response.text
    assert response.json()["data"][0]["file_id"] == payload["file_id"], response.text


def test_generate_api_key(test_client):
    new_key = {"email": "genapikey@test.com", "name": "testkey"}
    response = test_client.post("/generate_key", json=new_key)
    assert response.status_code == 200, response.text
    assert "api_key" in response.json(), response.text


def test_list_api_keys(test_client):
    response = test_client.get("/api_keys?email=listapikey@test.com")
    assert response.status_code == 200, response.text
    assert isinstance(response.json()["api_keys"], list), response.text


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
    assert response.status_code == 200, response.text
    assert "message" in response.json(), response.text
    assert response.json()["message"] == "API key deleted successfully", response.text


def test_get_metrics_with_valid_project(test_client):
    user_email = "voynow99@gmail.com"
    project_name = "test_project"
    params = {"user_email": user_email, "project_name": project_name}
    response = test_client.get("/get_metrics", params=params)
    assert response.status_code == 200, response.text

    response_data = response.json()

    for metric in response_data:
        assert "data" in metric, response.text
        assert "layout" in metric, response.text
        assert isinstance(metric["data"], list), response.text
        assert isinstance(metric["layout"], dict), response.text

        if metric["data"]:
            first_data = metric["data"][0]
            assert "line" in first_data, response.text
            assert "marker" in first_data, response.text
            assert "mode" in first_data, response.text
            assert "name" in first_data, response.text
            assert "x" in first_data, response.text
            assert "y" in first_data, response.text
            assert "type" in first_data, response.text


def test_list_projects(test_client):
    """Test /list_projects route with valid data"""
    user_email = "voynow99@gmail.com"
    params = {"user_email": user_email}
    response = test_client.get("/list_projects", params=params)

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), dict), response.text
    assert "projects" in response.json(), response.text
    for project in response.json()["projects"]:
        assert "name" in project, response.text
        assert "user" in project, response.text
        assert "is_active" in project, response.text
        assert project["is_active"] == True, response.text


def test_set_favorite_project(test_client):
    """Test /set_favorite_project route with valid data"""
    user_email = "voynow99@gmail.com"
    project_name = "maintainability"

    # Test setting a project as favorite
    response = test_client.post(
        "/set_favorite_project",
        json={"user_email": user_email, "project_name": project_name},
    )

    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": f"{project_name} set as favorite project"
    }, response.text


def test_get_user_email(test_client):
    """Test /get_user_email route with valid data"""
    user_email = "voynow99@gmail.com"
    params = {"email": user_email}
    response = test_client.get("/api_keys", params=params)
    key = response.json()["api_keys"][0]["api_key"]

    params = {"api_key": key}
    response = test_client.get(f"/get_user_email", params=params)
    assert response.status_code == 200, response.text
    assert response.json() == user_email, response.text


def test_get_user_email_with_invalid_api_key(test_client):
    """Test /get_user_email route with invalid data"""
    params = {"api_key": "invalid"}
    response = test_client.get(f"/get_user_email", params=params)
    assert response.status_code == 401, response.text


def test_fetch_repo_structure(test_client):
    params = {"user": "voynow", "repo": "turbo-docs"}
    response = test_client.get("/fetch_repo_structure", params=params)
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list), response.text


def test_fetch_file_content(test_client):
    params = {"user": "voynow", "repo": "turbo-docs", "path": "README.md"}
    response = test_client.get("/fetch_file_content", params=params)
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), str), response.text


def test_validate_github_project_not_found(test_client):
    params = {
        "user": "voynow99@gmail.com",
        "github_username": "voynow",
        "github_repo": "non-existent-repo",
    }
    response = test_client.post("/insert_project", params=params)
    assert response.status_code == 404, response.text


def test_validate_github_project_duplicate(test_client):
    params = {
        "user": "voynow99@gmail.com",
        "github_username": "voynow",
        "github_repo": "maintainability",
    }
    response = test_client.post("/insert_project", params=params)
    assert response.status_code == 400, response.text


def test_insert_delete_project(test_client):
    """
    Test insert and delete functionality by inserting an existing but inactive
    project and then deleting it
    """
    params = {
        "user": "voynow99@gmail.com",
        "github_username": "voynow",
        "github_repo": "turbo-docs",
    }

    # Check that project exists but is inactive
    start_status = io_operations.get_project_status(
        params["user"], params["github_username"], params["github_repo"]
    )
    assert start_status == models.ProjectStatus.INACTIVE

    # Insert project
    response = test_client.post("/insert_project", params=params)
    assert response.status_code == 200, response.text

    # Check that project exists and is active
    intermediate_status = io_operations.get_project_status(
        params["user"], params["github_username"], params["github_repo"]
    )
    assert intermediate_status == models.ProjectStatus.ACTIVE

    # Delete project
    response = test_client.post("/delete_project", params=params)
    assert response.status_code == 200, response.text

    # Check that project exists but is inactive
    end_status = io_operations.get_project_status(
        params["user"], params["github_username"], params["github_repo"]
    )
    assert end_status == models.ProjectStatus.INACTIVE


def test_insert_new_project(test_client):
    """
    Test insert and delete functionality by inserting a NEW project and then
    deleting it
    """
    params = {
        "user": "voynow99@gmail.com",
        "github_username": "voynow",
        "github_repo": "leet-learn-ai",
    }

    # Check that project does not exist
    start_status = io_operations.get_project_status(
        params["user"], params["github_username"], params["github_repo"]
    )
    assert start_status == models.ProjectStatus.NOT_FOUND

    # Insert project
    response = test_client.post("/insert_project", params=params)
    assert response.status_code == 200, response.text

    # Check that project exists and is active
    intermediate_status = io_operations.get_project_status(
        params["user"], params["github_username"], params["github_repo"]
    )
    assert intermediate_status == models.ProjectStatus.ACTIVE

    # Delete project
    io_operations.delete_project_for_testing(
        params["user"], params["github_username"], params["github_repo"]
    )

    # Check that project exists but is inactive
    end_status = io_operations.get_project_status(
        params["user"], params["github_username"], params["github_repo"]
    )
    assert end_status == models.ProjectStatus.NOT_FOUND
