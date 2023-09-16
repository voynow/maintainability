from dataclasses import dataclass


@dataclass
class MaintainabilityMetrics:
    readability: int
    design_quality: int
    testability: int
    consistency: int
    debug_error_handling: int


@dataclass
class FileMetrics:
    file_size: int
    loc: int
    language: str
    content: str


@dataclass
class CompositeMetrics:
    maintainability: MaintainabilityMetrics
    file_info: FileMetrics
    timestamp: str
    session_id: str
