from enum import StrEnum

class DeleteContentFileCategory(StrEnum):
    ADDONS = "addons"
    WORLDS = "worlds"

    def __str__(self) -> str:
        return str(self.value)
