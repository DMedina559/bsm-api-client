from enum import StrEnum

class GetEventActivityStatusType0(StrEnum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    DISPATCHING = "dispatching"
    PARTIAL = "partial"
    SUPPRESSED = "suppressed"

    def __str__(self) -> str:
        return str(self.value)
