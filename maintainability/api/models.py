from pydantic import BaseModel


class MaintainabilityMetrics(BaseModel):
    readability: int
    design_quality: int
    testability: int
    consistency: int
    debug_error_handling: int


class FileMetrics(BaseModel):
    file_size: int
    loc: int
    language: str
    content: str


class CompositeMetrics(BaseModel):
    maintainability: MaintainabilityMetrics
    file_info: FileMetrics
    timestamp: str
    session_id: str
