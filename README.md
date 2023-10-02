# Maintainability - Codebase Maintainability Analyzer

![GitHub stars](https://img.shields.io/github/stars/voynow/maintainability)
![PyPI](https://img.shields.io/pypi/v/maintainability)

Maintainability is a Python CLI -> API workflow that innovates on static code analysis using large language models (GPT). It provides a comprehensive analysis of your codebase's maintainability, focusing on readability, design quality, testability, consistency, and debug error handling. 

## Why Use Maintainability? 🚀

In the era of AI, why stick to traditional static code analysis? Maintainability leverages the power of GPT models to provide a more in-depth and intelligent analysis of your codebase. It's not just about finding bugs or syntax errors; it's about improving the quality of your code. 

Imagine a future where this tool is integrated into your CI/CD pipeline, continuously analyzing and improving your codebase. That's the future Maintainability is building towards.

## Repo Structure 📂

```
.
├── .github
│   └── workflows
│       ├── integration_tests.yaml
│       └── publish_package.yaml
├── maintainability
│   ├── api
│   │   ├── requirements.txt
│   │   ├── src
│   │   │   ├── main.py
│   │   │   ├── metrics_manager.py
│   │   │   ├── models.py
│   │   │   └── __init__.py
│   │   └── vercel.json
│   └── cli
│       ├── file_operations.py
│       ├── main.py
│       └── __init__.py
├── tests
│   ├── test_api_integration.py
│   └── test_cli_integration.py
├── integration_tests.sh
├── pyproject.toml
└── README.md
```

## Usage 💻

To use Maintainability, you can run it from the command line with the following command:

```bash
maintainability --paths /path/to/your/code
```

This will analyze the code at the specified path and return a comprehensive maintainability report.

## Example 📖

Here's an example of how you can use Maintainability to analyze a Python file:

```bash
maintainability --paths /path/to/your/python/file.py
```

This will return a maintainability report for `file.py`, providing insights into its readability, design quality, testability, consistency, and debug error handling.

## Future Plans 🌈

We're working towards integrating Maintainability into GitHub Actions as a CI/CD step. This will allow you to continuously analyze and improve your codebase's maintainability with every push.

Stay tuned for more updates!

## Contributing 🤝

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.