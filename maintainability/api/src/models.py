from pydantic import BaseModel


class MaintainabilityMetrics(BaseModel):
    readability: int = 0
    design_quality: int = 0
    testability: int = 0
    consistency: int = 0
    debug_error_handling: int = 0


class FileMetrics(BaseModel):
    file_size: int
    loc: int
    extension: str
    content: str


class CompositeMetrics(BaseModel):
    maintainability: MaintainabilityMetrics
    file_info: FileMetrics
    timestamp: str
    session_id: str
