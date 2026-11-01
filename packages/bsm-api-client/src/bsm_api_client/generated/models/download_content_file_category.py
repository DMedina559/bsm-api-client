from enum import StrEnum

class DownloadContentFileCategory(StrEnum):
    ADDONS = "addons"
    WORLDS = "worlds"

    def __str__(self) -> str:
        return str(self.value)
