import os
from datetime import datetime
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

os.environ["SKIP_AUTH_MIDDLEWARE"] = "True"
from api.src import main, io_operations, models

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
    payload = {
        "file_id": "88888888-8888-8888-8888-888888888888",
        "session_id": "88888888-8888-8888-8888-888888888888",
        "file_path": "/test/path/testfile.py",
        "content": "print('hello world')\n" * 100,
        "metric_name": "adaptive_resilience",
    }
    response = test_client.post("/extract_metrics", json=payload)
    assert response.status_code == 200, response.text
    assert "file_id" in response.json()
    assert response.json()["file_id"] == payload["file_id"], response.text


def test_insert_file(test_client):
    """Test /insert_file route with valid data"""
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
    response = test_client.post("/insert_file", json=payload)
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), dict), response.text
    assert response.json()["data"][0]["file_id"] == payload["file_id"], response.text


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


def test_check_file_criteria_valid(test_client):
    params = {"file_path": "utils/process.py", "extension": "py", "line_count": 150}
    response = test_client.post("/check_file_criteria", params=params)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "result": True,
        "message": "File meets criteria",
    }, response.text


def test_check_file_criteria_disallowed_extension(test_client):
    params = {
        "file_path": "main.unknown",
        "extension": "unknown",
        "line_count": 150,
    }
    response = test_client.post("/check_file_criteria", params=params)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "result": False,
        "message": "File extension not allowed",
    }, response.text


def test_check_file_criteria_insufficient_lines(test_client):
    params = {
        "file_path": "utils/process.py",
        "extension": "py",
        "line_count": 5,
    }
    response = test_client.post("/check_file_criteria", params=params)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "result": False,
        "message": "Insufficient number of lines",
    }, response.text


def test_check_file_criteria_test_file(test_client):
    params = {
        "file_path": "utils/process_test.py",
        "extension": "py",
        "line_count": 150,
    }
    response = test_client.post("/check_file_criteria", params=params)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "result": False,
        "message": "identified as test file.",
    }, response.text


def test_check_file_criteria_config_file(test_client):
    params = {"file_path": "utils/config.py", "extension": "py", "line_count": 150}
    response = test_client.post("/check_file_criteria", params=params)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "result": False,
        "message": "identified as config file.",
    }, response.text


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


def test_validate_github_project_whitelist(test_client):
    params = {
        "user": "unknownuser@gmail.com",
        "github_username": "voynow",
        "github_repo": "maintainability",
    }
    response = test_client.post("/insert_project", params=params)
    assert response.json() == {
        "detail": "You do not have permisions enabled to add this project."
    }


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
        "github_repo": "ConvNet-Architectures",
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
