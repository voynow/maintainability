## function: write_log_to_supabase
#### args: frame, message
This function is designed to write logs to Supabase. It extracts the filename and line number from the frame object and combines them to form a location string. The function then calls the `io_operations.write_log` method to write the log message to the specified location. This is particularly useful for tracking the execution of your code and identifying any potential issues.

## function: logger
#### args: message
The logger function is designed to log messages with the context of the caller frame. It retrieves the caller frame using Python's inspect module and then writes the log message along with the frame information to Supabase. This function is particularly useful for debugging and tracking the flow of execution, especially in complex systems where tracing the origin of a log message might be challenging.

