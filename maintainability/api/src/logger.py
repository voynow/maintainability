import inspect
from . import io_operations


def write_log_to_supabase(frame, message):
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    loc = f"{filename}:{lineno}"
    io_operations.write_log(loc, message)


def logger(message):
    frame = inspect.currentframe().f_back
    write_log_to_supabase(frame, message)
