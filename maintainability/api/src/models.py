from pydantic import BaseModel, Field
from datetime import datetime
import pytz
from uuid import UUID


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


class File(BaseModel):
    file_id: UUID = Field(default_factory=UUID)
    file_path: str
    project_name: str
    user_email: str
    file_size: int
    loc: int
    extension: str
    content: str
    timestamp: datetime
    session_id: UUID = Field(default_factory=UUID)


class Metric(BaseModel):
    primary_id: UUID = Field(default_factory=UUID)
    metric: str
    score: int
    reasoning: str
    file_id: UUID


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
