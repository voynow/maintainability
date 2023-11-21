import json
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field


class ExtractMetricsTransaction(BaseModel):
    file_id: UUID = Field(default_factory=UUID)
    session_id: UUID = Field(default_factory=UUID)
    file_path: str
    content: str
    metric_name: str


class Metric(BaseModel):
    primary_id: UUID = Field(default_factory=UUID)
    file_id: UUID = Field(default_factory=UUID)
    session_id: UUID = Field(default_factory=UUID)
    timestamp: datetime
    metric: str
    score: int
    reasoning: str

    class Config:
        json_encoders = {UUID: lambda v: str(v), datetime: lambda v: v.isoformat()}

    def model_dump(self, mode: str = "json", **kwargs) -> Any:
        """
        Custom serialization to handle the conversion of non-serializable types and
        additional formatting based on the 'mode'.
        """
        return json.loads(self.model_dump_json(**kwargs))


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

    class Config:
        json_encoders = {UUID: lambda v: str(v), datetime: lambda v: v.isoformat()}

    def model_dump(self):
        """
        Custom serialization to handle the conversion of non-serializable types.
        This replaces the deprecated '.dict()' method if it's no longer available.
        """
        return json.loads(self.model_dump_json(by_alias=True))


class Project(BaseModel):
    primary_id: UUID = Field(default_factory=UUID)
    name: str
    user: str
    created_at: datetime
    favorite: bool = Field(default=False)
    github_username: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)

    class Config:
        populate_by_name = True


class ProjectList(BaseModel):
    projects: Optional[list[Project]]


class ProjectStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    NOT_FOUND = "not found"


class FavoriteProjectRequest(BaseModel):
    user_email: str
    project_name: str


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


class APIKey(BaseModel):
    """API key information"""

    api_key: str
    user: str
    creation_date: str
    status: str = Field("active", description="active or inactive")
