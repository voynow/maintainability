# Maintainability API & CLI 🛠️

![GitHub stars](https://img.shields.io/github/stars/voynow/maintainability?style=social)
![PyPI](https://img.shields.io/pypi/v/maintainability)

Maintainability is a powerful tool that allows you to analyze the maintainability of your codebase. It provides a FastAPI based API and a command-line interface (CLI) to interact with the API. The application calculates various metrics related to code maintainability such as readability, design quality, testability, consistency, and debug error handling.

## Why Use Maintainability? 🚀

Maintainability is designed to help you improve the quality of your codebase. It provides you with detailed metrics about your code, which can help you identify areas that need improvement. By using Maintainability, you can ensure that your code is easy to understand, modify, and test, which can save you a lot of time and effort in the long run.

## Repo Structure 📂

```
maintainability
├── api
│   ├── requirements.txt
│   ├── src
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── test_main.py
│   │   └── utils.py
│   └── vercel.json
└── cli
    ├── cli.py
    └── __init__.py
```

## Usage 🖥️

### CLI

The CLI provides a simple way to interact with the API. Here's an example of how to use it:

```bash
python cli.py --paths /path/to/your/code
```

This command will analyze the code in the specified paths and return the maintainability metrics.

### API

The API provides two main endpoints:

- `POST /submit_metrics`: This endpoint allows you to submit your metrics to the API. Here's an example of how to use it:

```python
import requests

data = {
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
}

response = requests.post("http://localhost:8000/submit_metrics", json=data)
```

- `POST /extract_metrics`: This endpoint allows you to extract metrics from your code. Here's an example of how to use it:

```python
import requests

data = {"/test/path/testfile.py": "print('hello world')"}

response = requests.post("http://localhost:8000/extract_metrics", json=data)
```

## Conclusion 🎉

Maintainability is a powerful tool for improving the quality of your codebase. By providing detailed metrics about your code, it can help you identify areas that need improvement and ensure that your code is easy to understand, modify, and test. Give it a try today!