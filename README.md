
# Maintainability 🧠🔍

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version 1.0](https://img.shields.io/badge/version-1.0-blue)
![MIT License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/voynow/maintainability)

## 🌟 Introduction

Welcome to a new era of AI code analysis. Unlike traditional rule-based systems, this Python-based tool uses Language Models for a nuanced understanding of your codebase. Improve maintainability, readability, and overall code health without the rigid constraints of traditional systems. 

## 🚀 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Backend Overview](#-backend-overview)
- [Frontend Overview](#-frontend-overview)
- [Contributing](#-contributing)
- [Team](#-team)
- [License](#-license)

## 🌈 Features

- **Adaptive Code Analysis**: Leverage OpenAI's language models for a comprehensive review.
- **User Authentication**: Secure role-based access.
- **Metrics Storage**: All analysis results are securely stored in Supabase.
- **API Key Management**: Generate and manage API keys for your team.
- **Real-time Analytics**: A React-based front-end for all your metrics.

## 📚 Backend Overview

### Intent and High-Level Workflow

The pulse of this tool is its Python-based backend. Not only does it analyze your code, but it also takes care of user authentication, metrics storage, and much more. Here's a sneak peek into what happens under the hood:

1. **User Authentication**: As you log in, your credentials are securely verified.
2. **Code Repository Analysis**: Next, we sift through your code repositories. Don't worry; files you wish to exclude are respected.
3. **Code Maintainability Analysis**: This is where the magic happens. OpenAI's language models gauge the quality of your code.
4. **Metrics Storage**: All the data is then sent for safe-keeping into a Supabase database.

### File Groups Analysis

The backend is neatly divided into modules, each responsible for a different aspect of the system. From handling HTTP routes to logging, everything has its place.

#### Database Interactions (`io_operations.py`)

This part of the system is your liaison to the Supabase database. It takes care of metrics storage, user and API key management. 

#### Logging (`logger.py`)

Every action is logged, ensuring complete transparency and aiding in debugging.

#### HTTP Routes (`routes.py` and `routes_helper.py`)

Whether you're interacting via the web front-end or making an API call, these routes serve as the gateway to the system's functionality.

#### CLI (`file_operations.py` and `main.py`)

Batch processing your repositories or integrating into your CI/CD pipeline? The CLI has got you covered.

## 🎨 Frontend Overview

### Backend Communication

The React-based front-end is your window to the tool's analytical capabilities. Using Axios, it communicates with the backend for everything from user authentication to metrics retrieval.

### Routing and State Management

We use React Router for client-side routing and manage global state through `AppContext.js`.

### Styling

The UI is crafted with inline React styling complemented by Material UI components, making it sleek and user-friendly.

### Deployment

The application is ready for deployment with configurations specified in `vercel.json`.

## 🤝 Team

- Jamie Voynow
- Possibly You?

## 👩‍🚀 Contributing

We welcome contributions from everyone! Reach out to me on twitter [@jamievoynow](https://twitter.com/jamievoynow)

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
