import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_FILE_NAME = ".bsm_cli_config.json"
DEFAULT_BASE_URL = "http://127.0.0.1:11325"


def get_config_path() -> Path:
    """Gets the path to the configuration file."""
    return Path.home() / CONFIG_FILE_NAME


def load_config() -> Dict[str, Any]:
    """Loads the configuration from the config file."""
    config_path = get_config_path()
    if not config_path.exists():
        return {}
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(config: Dict[str, Any]):
    """Saves the configuration to the config file."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


class Config:
    """Manages CLI configuration."""

    def __init__(self):
        self._config = load_config()

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value."""
        # Prioritize environment variables
        env_var = f"BSM_{key.upper()}"
        value = os.environ.get(env_var)
        if value:
            if isinstance(default, bool):
                return value.lower() in ("true", "1", "yes")
            return value

        # Fallback to config file
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Sets a configuration value."""
        self._config[key] = value
        save_config(self._config)

    @property
    def base_url(self) -> str:
        """The API base URL."""
        return self.get("base_url", DEFAULT_BASE_URL)

    @property
    def verify_ssl(self) -> bool:
        """Whether to verify SSL."""
        return self.get("verify_ssl", True)

    @property
    def username(self) -> Optional[str]:
        """The username for authentication."""
        return self.get("username")

    @property
    def password(self) -> Optional[str]:
        """The password for authentication."""
        return self.get("password")

    @property
    def jwt_token(self) -> Optional[str]:
        """The JWT for authentication."""
        return self.get("jwt_token")

    @jwt_token.setter
    def jwt_token(self, value: Optional[str]):
        """Sets the JWT."""
        self.set("jwt_token", value)
