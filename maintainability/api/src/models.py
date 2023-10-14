from pydantic import BaseModel, Field


class ExtractMetrics(BaseModel):
    filepath: str
    file_content: str
    session_id: str


class ValidModelResponse(BaseModel):
    """LLM response validation model"""

    readability: int = 0
    design_quality: int = 0
    testability: int = 0
    consistency: int = 0
    debug_error_handling: int = 0


class Maintainability(BaseModel):
    """
    Composiiton of maintainability, file metrics, and user information
    TODO add user_id
    """

    file_path: str
    readability: int = 0
    design_quality: int = 0
    testability: int = 0
    consistency: int = 0
    debug_error_handling: int = 0
    file_size: int
    loc: int
    extension: str
    content: str
    session_id: str


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
