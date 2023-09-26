from fastapi.testclient import TestClient
from api.src import main

client = TestClient(main.app)


def test_submit_metrics():
    response = client.post(
        "/submit_metrics",
        json={
            "/test/path/testfile.py": {
                "maintainability": {
                    "readability": 0,
                    "design_quality": 0,
                    "testability": 0,
                    "consistency": 0,
                    "debug_error_handling": 0,
                },
                "file_info": {
                    "file_size": 0,
                    "loc": 0,
                    "language": "test",
                    "content": "test",
                },
                "timestamp": "test",
                "session_id": "88888888-8888-8888-8888-888888888888",
            }
        },
    )
    assert response.status_code == 200
    assert "status" in response.json()


def test_extract_metrics():
    response = client.post(
        "/extract_metrics",
        json={"/test/path/testfile.py": "print('hello world')"},
    )
    assert response.status_code == 200
