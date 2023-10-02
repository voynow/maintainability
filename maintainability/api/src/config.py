PROMPT = """You are a highly respected tech lead participating in a code review of {filepath}:
{code}

Be strict and critical. Evaluate this code across key maintainability metrics:
readability: Ease to understand. Includes comments. 1=Hard, 10=Easy
design quality: Adherence to single-responsibility and complexity of functions. 1=Poor, 10=Excellent
testability: Ease to write unit tests. 1=Hard, 10=Easy
consistency: Naming and coding conventions. 1=Inconsistent, 10=Consistent
debug & error handling: Availability of logs and error-handling. 1=Poor, 10=Excellent

Respond with JSON only, no other text or comments, with the following keys:
readability, design_quality, testability, consistency, debug_error_handling
"""

MIN_NUM_LINES = 20
OUTPUT_FILE = "output.json"
MODEL_NAME = "gpt-3.5-turbo-16k"
TEMPERATURE = 0.0
