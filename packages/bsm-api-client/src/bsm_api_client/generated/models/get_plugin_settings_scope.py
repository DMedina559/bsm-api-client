from enum import StrEnum

class GetPluginSettingsScope(StrEnum):
    GLOBAL = "global"
    PLUGIN = "plugin"
    SERVER = "server"

    def __str__(self) -> str:
        return str(self.value)
