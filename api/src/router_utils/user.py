import base64
import secrets

from fastapi import HTTPException
from passlib.context import CryptContext

from .. import io_operations, logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_user(email: str, password: str) -> None:
    user = io_operations.get_user(email)

    if not user or not pwd_context.verify(password, user["password"]):
        logger.logger(f"Unauthorized login attempt: email={email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")


def generate_new_api_key():
    random_bytes = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")


def generate_api_key_helper():
    api_key = generate_new_api_key()
    while io_operations.select_api_key(api_key):
        api_key = generate_new_api_key()
    return api_key
