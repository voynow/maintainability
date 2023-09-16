import os
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
    language: str
    loc: int


@dataclass
class GeneralMetrics:
    project_name: str
    timestamp: str


@dataclass
class CompositeMetrics:
    maintainability: MaintainabilityMetrics
    file_info: FileMetrics
    general_info: GeneralMetrics
