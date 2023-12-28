# Maintainability - AI Driven Code Analysis 📈

Maintainability is a comprehensive platform that leverages advanced language models to go beyond traditional static code analysis systems. Our platform offers nuanced understanding and insightful metrics to help you write more maintainable, secure, and efficient code.

## Getting Started 🚀

### Prerequisites

Before you start using Maintainability, make sure you have the following installed:

- **Node.js**: You'll need Node.js to run the development server. You can download it from [here](https://nodejs.org/).
- **npm**: Node.js package manager, comes with Node.js installation.

### Installation

1. Clone this repository or download the source code.
   ```sh
   git clone https://github.com/your-username/maintainability.git
   ```
2. Navigate to the `webapp` directory in your terminal.
3. Install the dependencies.
   ```sh
   npm install
   ```
4. Start the development server.
   ```sh
   npm start
   ```

### Environment Setup

Two environment files are used, one for development and one for production:

- `.env.development`: For local development server.
- `.env.production`: For production server.

Make sure to have the `REACT_APP_API_URL` variable set in these files to point to the correct API endpoints.

## Usage 🖥️

After starting the development server, you can:

- **Sign Up**: Create your account to start analyzing your projects.
- **Log In**: Securely access your dashboard.
- **Analyzing Projects**: Add your GitHub repositories to analyze and receive insights and metrics on the code quality.

### Features

- **Intuitive Design**: Clear metrics on naming conventions, comment quality and API usability.
- **Functional Cohesion**: Ensures single responsibility and separation of concerns are maintained in the codebase.
- **Adaptive Resilience**: Tracks error-handling, resource management, and adaptability of code.
- **Code Efficiency**: Monitors algorithmic complexity and optimizes resource utilization.
- **Data Integrity**: Validates data handling and security.

### Configuration

Tailwind CSS is used for styling. Customize the `tailwind.config.js` to fit your design needs.

### Deployment

The `vercel.json` file is configured for deploying with Vercel. You can adjust the routes and headers if you have specific caching or routing needs.

## Development 🛠️

### File Structure

- **Components**: React components are located under `src/components`.
- **Context**: App-wide state management is handled in `src/AppContext.js`.
- **API Configuration**: Axios instance with request interceptors is set up in `src/axiosConfig.js`.
- **Styles**: Global styles are written in `src/index.css`.

### Adding a New Feature

To add a new feature, create a new branch and follow these steps:

1. Write your feature code.
2. Write unit tests to ensure the feature works as expected.
3. Update documentation if necessary.
4. Create a Pull Request (PR) for review.

### PR Review Process

All PRs should be reviewed by at least one maintainer. Ensure that:

- Code quality checks pass.
- Test coverage is adequate.
- The feature is documented.

### Running Tests

To run existing tests, use the following command:

```sh
./integration_tests.sh
```

## Contributing 🤝

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## License 📝

Distributed under the MIT License. See `LICENSE` for more information.

## Contact 📮

If you have any queries or suggestions, please feel free to contact me at voynow99@gmail.com or connect with me on X @jamievoynow.

---

Made with ❤️ and ☕ by [Jamie Voynow](https://github.com/voynow)
