from dataclasses import dataclass


@dataclass
class MaintainabilityMetrics:
    Readability: int
    Design_Quality: int
    Testability: int
    Consistency: int
    Debug_Error_Handling: int
