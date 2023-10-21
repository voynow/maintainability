## function: call_api_wrapper
#### args: base_url, endpoint, payload, api_key
The `call_api_wrapper` function is a robust utility for making API calls. It constructs the URL from a base URL and an endpoint, sends a POST request with an optional payload, and handles any HTTP or unexpected errors. The function also supports API keys for authenticated requests and logs any errors encountered during the request, making it easier to debug and understand the issues.

## function: extract_metrics
#### args: project_name, session_id, filepath, content, base_url, api_key
The `extract_metrics` function is designed to send a specific file from a project to an API endpoint for metric extraction. It logs the process, sends the file, and logs the response. This function is particularly useful for automating the process of metric extraction from multiple files in a project, and it handles the API calls and logging in a streamlined manner.

## function: cli_runner
#### args: paths, base_url, api_key
The `cli_runner` function is a command-line interface tool that initiates the extraction of metrics from specified file paths within a project. It generates a unique session ID for each run, loads files from the repository, filters the repository based on the target paths, and then extracts metrics for each file. This function is particularly useful for batch processing of files and can be customized with different base URLs and API keys.

