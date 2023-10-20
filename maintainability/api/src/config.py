PROMPT = """You are a highly respected tech lead participating in a code review of {filepath}:
{code}

Evaluate this code as follows:
{metric_description}

Write two-three bullet points on your initial thoughts. When you are done, conclude with a numerical response (X/10 where 10 is perfect and 0 is bad) and nothing else.
"""

METRIC_DESCRIPTIONS = {
    "semantic clarity": """Definition: Measures how well the code communicates its deeper intentions and logic.
        Criteria for Labeling:
        Variable Naming: Variables must be named to indicate their purpose and type. E.g., user_count instead of uc or temp.
        Function Naming: Functions must indicate what they do and what they return. E.g., calculate_total_price() instead of calc() or process().
        Comment Quality: Comments should explain the why. E.g., # Caching result for performance instead of # Storing x.
        Code Organization: Logical structure is mandatory. E.g., grouping all database-related functions together.
        Quantifiable Aspects: Percentage of variables and functions that meet these standards, relevance and clarity of comments, logical flow of code.""",
    "functional cohesion": """Definition: Measures how functions or modules focus on single, well-defined tasks.
        Criteria for Labeling:
        Responsibility Count: Each function should have one task. E.g., sort_array() shouldn't also update a database.
        Separation of Concerns: UI logic and data manipulation must be separate. E.g., MVC pattern.
        Quantifiable Aspects: Number of functions violating single-responsibility, separation of concerns in functions.""",
    "adaptive resilience": """Definition: Assesses code's adaptability to different operational scenarios.
        Criteria for Labeling:
        Error-Handling: Use try-catch for all external calls. E.g.,
        try:
        response = requests.get(url)
        except requests.HTTPError as err:
        handle_error(err)
        Resource Management: Explicitly manage all resources. E.g., use with open("file.txt") as f: to ensure file closure.
        Adaptability: Features like auto-scaling must be present. E.g., AWS Lambda auto-scaling settings.
        Quantifiable Aspects: Adequacy of error-handling, resource management techniques, adaptability features.""",
    "code efficiency": """Definition: Assesses computational and memory efficiency.
        Criteria for Labeling:
        Algorithmic Complexity: Algorithms worse than O(n log n) must be justified. E.g., avoid nested loops for simple tasks.
        Resource Utilization: Optimize memory and CPU. E.g., using list comprehensions instead of loops for simple transformations.
        Optimization: Profile for bottlenecks and optimize. E.g., using cProfile for Python code profiling.
        Quantifiable Aspects: Identify violating algorithms, measure memory and CPU usage, flag unoptimized code.""",
    "api usability": """Definition: Evaluates usability of all interfaces, both public and private.
        Criteria for Labeling:
        Naming Conventions: Clear method names. E.g., get_user_by_id() instead of get_user().
        Parameter Types: Minimum parameters with clear types. E.g., def process_data(data: List[int]) -> None: instead of def process_data(data):.
        Return Types: Clear return types. E.g., def calculate_price() -> float:.
        Quantifiable Aspects: Intuitiveness of method names, parameter count and types, appropriateness of return types.""",
    "data security and integrity": """Definition: Assesses data security and integrity.
        Criteria for Labeling:
        Data Validation: All user inputs must be validated. E.g.,
        if not re.match("^[a-zA-Z0-9_]*$", username):
        raise ValueError("Invalid username")
        Data Sanitation: Sanitize all data. E.g., parameterized SQL queries to prevent SQL injection.
        Password and API Key Security: Sensitive information must be encrypted. E.g., using Python's cryptography library for encryption.
        Quantifiable Aspects: Presence of data validation, effectiveness of data sanitation, security measures for sensitive information.""",
}

METRIC_COLS = [
    "readability",
    "design_quality",
    "testability",
    "consistency",
    "debug_error_handling",
]

MODEL_NAME = "gpt-3.5-turbo-16k"
TEMPERATURE = 0.0
