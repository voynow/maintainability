# Maintainability 🚀

![GitHub](https://img.shields.io/github/license/voynow/maintainability)
![GitHub last commit](https://img.shields.io/github/last-commit/voynow/maintainability)

Unlock the full potential of your codebase! Our platform offers an end-to-end solution to analyze, track, and elevate your code quality. 

## 📌 Main Components

1. **🌐 API**: The powerhouse of our platform. Provides robust endpoints for metrics, user management, and more.
2. **💻 CLI**: Your local companion for fetching key metrics from your codebase and sending them effortlessly to our API.
3. **🖥️ Frontend**: An intuitive dashboard for real-time insights and management of your account and API keys.

---

## 🌐 API

Built with FastAPI and backed by a Supabase database, our API is engineered for performance and scalability.

### 📂 Structure

- `main.py`: Kick-starts the FastAPI application, sets CORS, and routes.
- `io_operations.py`: Your one-stop for all database operations and logging.
- `metrics_manager.py`: Where the magic happens! Handles all metrics calculations.
- `models.py`: Defines Pydantic models for rock-solid data validation.
- `routes.py`: Home to various API functionalities.
- `routes_helper.py`: Assists in route operations. Think of it as your API's best friend.

### 🎯 Purpose

The API is the backbone, offering all functionalities from metrics calculation to user management.

---

## 💻 CLI

Designed for ease of use, our CLI tool is all about bringing metrics to your fingertips.

### 📂 Structure

- `main.py`: The command center of the CLI.
- `file_operations.py`: Reads files and honors `.gitignore`.

### 🎯 Purpose

The CLI is the data collector in our ecosystem, making it a breeze to send metrics to the centralized API.

---

## 🖥️ Frontend

Built with React, our frontend is all about delivering a user-friendly experience.

### 📂 Structure

- `App.js`: The main hub for routing and global state.
- `components/`: Houses all UI components like Login, Register, and APIKeys.
- `AppContext.js`: Manages global state via React Context.
- `axiosConfig.js`: Configures global settings for API calls.

### 🎯 Purpose

The frontend provides a seamless interface for users to manage and view metrics, API keys, and more.

---

## 🌟 Overall Purpose

The Maintainability Analytics Platform aims to be your go-to solution for code quality. 📈 Elevate your codebase by collecting metrics through our CLI, managing data via our robust API, and visualizing insights through our web frontend.

Join us in making code better, one metric at a time! 🤝