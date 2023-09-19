from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_submit_metrics():
    response = client.post(
        "/submit_metrics",
        json={
            "/test/path/testfile.py": {
                "maintainability": {
                    "readability": 1,
                    "design_quality": 2,
                    "testability": 3,
                    "consistency": 4,
                    "debug_error_handling": 5,
                },
                "file_info": {
                    "file_size": 1000,
                    "loc": 100,
                    "language": "python",
                    "content": "print('hello world')",
                },
                "timestamp": "timestamp",
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
    print("Hello0000")
    print("Hello", response.json())
    assert response.status_code == 200
