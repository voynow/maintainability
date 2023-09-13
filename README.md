# Maintainability

Maintainability is a Python application that analyzes the maintainability of your codebase. It provides metrics such as readability, design quality, testability, consistency, and debug error handling for each file in your repository.

## 📚 Table of Contents
- [Why Use Maintainability](#why-use-maintainability)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## 🎯 Why Use Maintainability
Maintainability is a key aspect of any software project. This tool helps you to keep track of the maintainability of your codebase, providing you with valuable insights that can guide your refactoring efforts. It's easy to use and integrates seamlessly into your development workflow.

## 🏗️ Repository Structure
```
maintainability
├── maintainability
│   ├── __init__.py
│   ├── app.py
│   ├── cli.py
│   ├── models.py
│   ├── utils.py
├── metrics.json
├── test_package_install.sh
```

## 💻 Installation
To install the Maintainability Analyzer, you can use pip:
```bash
pip install maintainability
```

## 🚀 Usage
To analyze the maintainability of your codebase, simply run the following command in your terminal:
```bash
maintainability
```
This will generate a `metrics.json` file in your current directory, containing the maintainability metrics for each file in your repository.

## 🤝 Contributing
Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.

## 📝 License
This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file for details.