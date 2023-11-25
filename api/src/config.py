# configs for LLM
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.0

# configs for file analysis
MIN_NUM_LINES = 50
EXTENSIONS = [
    ".py",
    ".js",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".cs",
    ".go",
    ".rb",
    ".php",
    ".swift",
    ".ts",
    ".kt",
    ".rs",
    ".scala",
    ".m",
    ".sh",
    ".sql",
    ".html",
    ".css",
]

# prompt template
PROMPT = """You are a highly respected tech lead at a leading technology company, participating in a code review of {filepath}:
{code}

Evaluate the code on {metric}:
{description}

Approach this review with big tech, production-ready expectations. Be uncompromising and severe in your critique. Use a zero-tolerance policy for lapses in quality, and make sure to distribute your scores rigorously and evenly across the 0-10 range. Reserve scores of 8, 9 or 10 for exceptional code that could be considered a best-in-class example. Reserve scores of 0, 1 or 2 for code that is entry-level, amateurish, or otherwise unacceptable.

Write two-three bullet points on your initial thoughts while being as brief as possible. When you are done, conclude with a numerical response (X/10, where 10 is exceptional and 0 is unacceptable) and nothing else.
"""

# prompts for metric descriptions
METRICS = {
    "intuitive_design": """Variable and Function Naming: Clear names indicating purpose and type.
Good: total_amount, calculate_tax(income)
Bad: ta, calc()

Comment Quality: Comments clarify the 'why,' not just the 'what.'
Good: "Using binary search for performance."
Bad: "Incrementing counter."

Code Organization: Logical structuring is key, extending to function and class organization.
Good: Methods in a class organized by functionality.
Bad: Disorganized mix of functions and classes.

API Usability: Includes intuitiveness, documentation quality, and new developer onboarding.
Good: Self-explanatory method names, documented parameters.
Bad: Poorly documented functions, ambiguous parameters.

Code Simplicity: Aim for straightforward code without sacrificing functionality.
Good: Using list comprehensions instead of simple for-loops.
Bad: Nested loops and if-statements that could be simplified.""",
    "functional_cohesion": """Single Responsibility Principle: Each function or module should have one, and only one, reason to change. This means it should perform one logical task.
Good: A function named calculate_tax(income) that only calculates tax.
Bad: A function named process_user_data() that validates input, updates a database, and sends email.

Separation of Concerns: Different aspects of the program should be separated into distinct sections of the codebase. This involves following established architectural patterns.
Good: Using MVC to separate data handling from business logic and UI.
Bad: Functions that mix database queries, business logic, and UI updates.

Function Length: While not a hard rule, aim for shorter functions when possible to make the code more readable and maintainable.
Good: Functions that are less than 20 lines of code.
Bad: Functions that are several hundred lines long.

Module Cohesion: Functions within a module should be strongly related in functionality. Avoid "god" modules that do everything.
Good: A PaymentProcessing module that only contains functions related to payment.
Bad: A Utilities module that contains everything from string manipulation to network requests.""",
    "adaptive_resilience": """Error-Handling: Employ comprehensive error-handling mechanisms, not just for external calls but also for internal logic that is prone to failure.
Good: Using try-except blocks around not just HTTP requests but also file operations, database calls, and any segments where exceptions might occur.
Bad: Only using error-handling for network requests but ignoring it for file I/O or other risky operations.

Graceful Degradation: Code should still function, albeit at a reduced level, even when some subsystems or services fail.
Good: Implementing circuit breakers or fallback methods when a dependent service is down.
Bad: No handling for scenarios where a dependent service is unavailable, leading to complete failure.

Resource Management: Explicitly manage all resources, not just file handles. This includes connections, memory, and even thread management.
Good: Using context managers like with in Python for file operations, database connections, and thread locks.
Bad: Leaving files open, database connections unclosed, or locks unreleased.

Adaptability: Ensure the code can adapt to different conditions, including load and data variability.
Good: Implementing auto-scaling, rate-limiting, and data partitioning to handle different operational scenarios.
Bad: Writing code that can't handle varying loads or data sizes.""",
    "code_efficiency": """Algorithmic Complexity: Use efficient algorithms and data structures. Complexity worse than O(n logn) should be justified.
Good: Using quicksort or mergesort for sorting tasks.
Bad: Using bubble sort for a large dataset without justification.

Resource Utilization: Monitor CPU and memory usage and minimize their footprint.
Good: Utilizing list comprehensions or generators in Python for more efficient memory use.
Bad: Using regular loops that create additional variables and take up more memory for simple tasks.

Runtime Profiling: Actively profile code to identify bottlenecks.
Good: Using tools like cProfile or timeit in Python to find slow segments of code.
Bad: Not measuring performance or ignoring bottlenecks.

Concurrency: Make use of parallelism and asynchronous programming where appropriate.
Good: Using Python's asyncio for I/O-bound tasks or ThreadPoolExecutor for CPU-bound tasks.
Bad: Running all tasks sequentially in a single-threaded environment when concurrency could be beneficial.

Data Fetching and Caching: Optimize how data is retrieved and stored.
Good: Implementing caching mechanisms or using batch retrieval for database calls.
Bad: Making frequent, repetitive calls to a database for the same data.""",
    "data_security_and_integrity": """Data Validation: Validate all user inputs at both client and server sides. This is not just about format but also about acceptable ranges or values.
Good: Using regex to validate usernames and also checking for banned or reserved names.
Bad: Only using front-end validation, which can be bypassed.

Data Sanitation: Ensure that all data is sanitized to prevent injection attacks, and not just SQL injections.
Good: Using parameterized SQL queries, HTML entity encoding for web views.
Bad: Concatenating user inputs directly into SQL queries or HTML views.

Password and API Key Security: All sensitive information should not just be encrypted but also securely stored and transmitted.
Good: Storing hashed passwords using strong algorithms like bcrypt, and keeping API keys in environment variables or secure key vaults.
Bad: Storing passwords in plaintext or keeping API keys hard-coded in the codebase.

Data Integrity Checks: Implement controls to ensure data is not tampered with during storage or transmission.
Good: Using checksums or digital signatures to verify data integrity.
Bad: No mechanisms in place to check if data has been altered or corrupted.

Least Privilege Access: Implement the principle of least privilege across the codebase.
Good: Assigning minimal required permissions for database access, file operations, and API calls.
Bad: Using a single admin-level account for all database operations, irrespective of the operation's sensitivity.

Logging and Monitoring: Keep detailed logs for security-relevant events and set up automated monitoring and alerts for unusual activities.
Good: Logging failed login attempts and setting up alerts for multiple failures from the same IP.
Bad: No logging or monitoring in place for security-relevant activities.""",
}

WHITELIST = [
    "voynow99@gmail.com",
]
