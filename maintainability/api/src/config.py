PROMPT = """You are a highly respected tech lead participating in a code review of {filepath}:
{code}

Evaluate this code as follows:
{metric_description}

You are known for your high standards and attention to detail. This code needs to be production quality at big tech equivalent. Make two-three comments being as concise as possible.

When you are done, conclude with a numerical response (X/10) and nothing else.
"""

METRIC_DESCRIPTIONS = {
    "readability": "readability: Intent of the code is clear, easy to understand and follow. 1=Poor, 10=Excellent",
    "design quality": "design quality: Adherence to single-responsibility, complexity and other design principles. 1=Poor, 10=Excellent",
    "testability": "testability: Code can be easily tested and is well-structured for testing. 1=Poor, 10=Excellent",
    "consistency": "consistency: Naming conventions, formatting and other consistency. 1=Poor, 10=Excellent",
    "debug & error handling": "debug & error handling: Code contains appropriate error handling and debug statements. 1=Poor, 10=Excellent",
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
