from pydantic import BaseModel, Field


class MaintainabilityMetrics(BaseModel):
    """various dimensions of code maintainability"""

    readability: int = 0
    design_quality: int = 0
    testability: int = 0
    consistency: int = 0
    debug_error_handling: int = 0


class FileMetrics(BaseModel):
    """File analysis metadata and content"""

    file_size: int
    loc: int
    extension: str
    content: str


class CompositeMetrics(BaseModel):
    """
    Composiiton of maintainability, file metrics, and user information
    TODO add user_id
    """

    maintainability: MaintainabilityMetrics
    file_info: FileMetrics
    timestamp: str
    session_id: str


class User(BaseModel):
    """user information including roles and API key"""

    username: str
    hashed_password: str = Field(..., alias="password")
    role: str


class Token(BaseModel):
    """JWT token information"""

    access_token: str
    token_type: str  # generally 'bearer'
