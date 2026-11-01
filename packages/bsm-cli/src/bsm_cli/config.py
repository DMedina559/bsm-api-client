import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_FILE_NAME = ".bsm_cli_config.json"
DEFAULT_BASE_URL = "http://127.0.0.1:11325"


def get_config_path() -> Path:
    """Gets the path to the configuration file."""
    return Path.home() / CONFIG_FILE_NAME


def protect_config(path: Path) -> None:
    """Protect persisted credentials before reading or writing their bytes."""
    if path.is_symlink():
        raise OSError("CLI credential file must not be a symbolic link")
    if os.name != "nt":
        path.chmod(0o600)
        return
    import ntsecuritycon
    import win32api
    import win32con
    import win32security

    token = win32security.OpenProcessToken(
        win32api.GetCurrentProcess(), win32con.TOKEN_QUERY
    )
    try:
        owner = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
    finally:
        token.Close()
    acl = win32security.ACL()
    for sid in (
        owner,
        win32security.CreateWellKnownSid(
            win32security.WinBuiltinAdministratorsSid, None
        ),
        win32security.CreateWellKnownSid(win32security.WinLocalSystemSid, None),
    ):
        acl.AddAccessAllowedAceEx(
            win32security.ACL_REVISION, 0, ntsecuritycon.FILE_ALL_ACCESS, sid
        )
    win32security.SetNamedSecurityInfo(
        str(path),
        win32security.SE_FILE_OBJECT,
        win32security.DACL_SECURITY_INFORMATION
        | win32security.PROTECTED_DACL_SECURITY_INFORMATION,
        None,
        None,
        acl,
        None,
    )


def load_config() -> Dict[str, Any]:
    """Loads the configuration from the config file."""
    config_path = get_config_path()
    if config_path.is_symlink():
        raise OSError("CLI credential file must not be a symbolic link")
    if not config_path.exists():
        return {}
    protect_config(config_path)
    try:
        with config_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_config(config: Dict[str, Any]):
    """Atomically save configuration with owner-only permissions."""
    import tempfile

    config_path = get_config_path()
    if config_path.is_symlink():
        raise OSError("CLI credential file must not be a symbolic link")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        # NamedTemporaryFile defaults to restrictive permissions on POSIX.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=config_path.parent,
            prefix=f".{config_path.name}.",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            protect_config(temporary_path)
            json.dump(config, handle, indent=4)
            handle.flush()
            os.fsync(handle.fileno())
        protect_config(temporary_path)
        os.replace(temporary_path, config_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


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

    def update(self, **values: Any) -> None:
        """Save related configuration values in one write."""
        updated = {**self._config, **values}
        save_config(updated)
        self._config = updated

    @property
    def base_url(self) -> str:
        """The API base URL."""
        return str(self.get("base_url", DEFAULT_BASE_URL))

    @property
    def verify_ssl(self) -> bool:
        """Whether to verify SSL."""
        return bool(self.get("verify_ssl", True))

    @property
    def username(self) -> Optional[str]:
        """The username for authentication."""
        val = self.get("username")
        return str(val) if val is not None else None

    @property
    def password(self) -> Optional[str]:
        """The password for authentication."""
        val = self.get("password")
        return str(val) if val is not None else None

    @property
    def jwt_token(self) -> Optional[str]:
        """The JWT for authentication."""
        val = self.get("jwt_token")
        return str(val) if val is not None else None

    @jwt_token.setter
    def jwt_token(self, value: Optional[str]):
        """Sets the JWT."""
        self.set("jwt_token", value)

    def trusted_device(
        self, username: Optional[str] = None, backend: Optional[str] = None
    ) -> Optional[str]:
        """Return a finite remembered factor only for its account and destination."""
        import time

        if username is None and any(
            os.environ.get(key)
            for key in ("BSM_JWT_TOKEN", "BSM_USERNAME", "BSM_PASSWORD")
        ):
            return None
        owner = username or self.get("active_username")
        if not owner or owner != self.get("trusted_device_owner"):
            return None
        if (backend or self.base_url).rstrip("/") != str(
            self.get("trusted_device_backend", "")
        ).rstrip("/"):
            return None
        expiry = self.get("trusted_device_expires_at")
        if not isinstance(expiry, (int, float)) or expiry <= time.time():
            return None
        token = self.get("trusted_device_token")
        return token if isinstance(token, str) and token.startswith("bsm_td_") else None
