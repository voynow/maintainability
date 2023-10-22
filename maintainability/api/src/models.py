from pydantic import BaseModel, Field
from datetime import datetime
import pytz
import uuid


class ExtractMetrics(BaseModel):
    file_id: str
    filepath: str
    file_content: str
    metric: str


class MetricTransaction(BaseModel):
    metric: str
    score: int
    reasoning: str
    file_id: str


class FileTransaction(BaseModel):
    file_id: str
    user_email: str
    project_name: str
    file_path: str
    file_size: int
    loc: int
    extension: str
    content: str
    session_id: str
    timestamp: str = datetime.now(pytz.utc).isoformat()


class GetMetricsResponse(BaseModel):
    """Response object for get_metrics route"""

    intuitive_design: float
    functional_cohesion: float
    adaptive_resilience: float
    code_efficiency: float
    data_security_and_integrity: float


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
