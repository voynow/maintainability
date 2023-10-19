PROMPT = """You are a highly respected tech lead participating in a code review of {filepath}:
{code}

Be strict and critical. Evaluate this code as follows:
{metric_description}

Respond with JSON only, no other text or comments, with the following keys:
readability, design_quality, testability, consistency, debug_error_handling
"""

METRIC_DESCRIPTIONS = {
    "readability": "readability: Ease to understand. Includes comments. 1=Hard, 10=Easy",
    "design quality": "design quality: Adherence to single-responsibility and complexity of functions. 1=Poor, 10=Excellent",
    "testability": "testability: Ease to write unit tests. 1=Hard, 10=Easy",
    "consistency": "consistency: Naming and coding conventions. 1=Inconsistent, 10=Consistent",
    "debug & error handling": "debug & error handling: Availability of logs and error-handling. 1=Poor, 10=Excellent",
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
