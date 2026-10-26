from enum import StrEnum

class GetEventActivityPhaseType0(StrEnum):
    AFTER = "after"
    BEFORE = "before"
    CUSTOM = "custom"
    LIFECYCLE = "lifecycle"

    def __str__(self) -> str:
        return str(self.value)
