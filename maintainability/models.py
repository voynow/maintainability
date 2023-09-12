from dataclasses import dataclass


@dataclass
class MaintainabilityMetrics:
    readability: int
    design_quality: int
    testability: int
    consistency: int
    debug_error_handling: int
