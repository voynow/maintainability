import inspect
import uuid
from . import io_operations

session_id = str(uuid.uuid4())


def write_log_to_supabase(frame, message):
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    loc = f"{filename}:{lineno}"
    io_operations.write_log(loc, message, session_id)


def logger(message):
    frame = inspect.currentframe().f_back
    write_log_to_supabase(frame, message)
