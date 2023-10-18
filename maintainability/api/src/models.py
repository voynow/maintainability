from pydantic import BaseModel, Field
from datetime import datetime
import pytz


class ExtractMetrics(BaseModel):
    project_name: str
    session_id: str
    filepath: str
    file_content: str


class ValidModelResponse(BaseModel):
    """LLM response validation model"""

    readability: int = -1
    design_quality: int = -1
    testability: int = -1
    consistency: int = -1
    debug_error_handling: int = -1


class Maintainability(BaseModel):
    """Composiiton of maintainability, file metrics, and user information"""

    user_email: str
    project_name: str
    file_path: str
    file_size: int
    loc: int
    extension: str
    content: str
    session_id: str
    readability: int
    design_quality: int
    testability: int
    consistency: int
    debug_error_handling: int
    timestamp: str = datetime.now(pytz.utc).isoformat()


class User(BaseModel):
    """user information"""

    email: str
    password: str  # hashed password
    role: str


class TokenRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    """JWT token information"""

    access_token: str
    token_type: str  # generally 'bearer'


class APIKey(BaseModel):
    """API key information"""

    api_key: str
    user: str
    creation_date: str
    status: str = Field("active", description="active or inactive")
