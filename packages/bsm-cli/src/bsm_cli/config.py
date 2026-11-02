import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_FILE_NAME = ".bsm_cli_config.json"
DEFAULT_BASE_URL = "http://127.0.0.1:11325"
SERVICE_NAME = "bsm-cli"
SECRET_KEYS = ("jwt_token", "trusted_device_token")


def get_config_path() -> Path:
    """Gets the path to the configuration file."""
    return Path.home() / CONFIG_FILE_NAME


def _os_secret_store_enabled(config_path: Optional[Path] = None) -> bool:
    """Use the OS credential store by default without polluting isolated test files."""
    mode = os.environ.get("BSM_CREDENTIAL_STORE", "").strip().lower()
    if mode in {"file", "none", "0", "false"}:
        return False
    if mode in {"os", "keyring", "1", "true"}:
        return True
    if "PYTEST_CURRENT_TEST" in os.environ:
        return False
    target = config_path or get_config_path()
    return target == (Path.home() / CONFIG_FILE_NAME)


def write_secret(  # noqa: C901
    key: str, value: Optional[str], *, service: str = SERVICE_NAME
) -> bool:
    """Store a secret in the OS credential manager; return True on success."""
    if not value:
        return delete_secret(key, service=service)
    try:
        import keyring  # type: ignore[import-not-found]

        keyring.set_password(service, key, value)
        return True
    except Exception:
        pass

    if os.name == "nt":
        try:
            import win32cred

            win32cred.CredWrite(
                {
                    "Type": win32cred.CRED_TYPE_GENERIC,
                    "TargetName": f"{service}:{key}",
                    "UserName": service,
                    "CredentialBlob": value,
                    "Persist": win32cred.CRED_PERSIST_LOCAL_MACHINE,
                },
                0,
            )
            return True
        except Exception:
            return False

    if sys.platform == "darwin":
        try:
            subprocess.run(
                [
                    "/usr/bin/security",
                    "add-generic-password",
                    "-U",
                    "-s",
                    service,
                    "-a",
                    key,
                    "-w",
                    value,
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False

    try:
        subprocess.run(
            [
                "secret-tool",
                "store",
                f"--label={service}",
                "service",
                service,
                "account",
                key,
            ],
            input=value.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def read_secret(  # noqa: C901
    key: str, *, service: str = SERVICE_NAME
) -> Optional[str]:
    """Read a secret from the OS credential manager if available."""
    try:
        import keyring  # type: ignore[import-not-found]

        val = keyring.get_password(service, key)
        if isinstance(val, str) and val:
            return val
    except Exception:
        pass

    if os.name == "nt":
        try:
            import win32cred

            cred = win32cred.CredRead(f"{service}:{key}", win32cred.CRED_TYPE_GENERIC)
            blob = cred.get("CredentialBlob")
            if isinstance(blob, bytes):
                return blob.decode("utf-16le")
            if isinstance(blob, str):
                return blob
        except Exception:
            return None

    if sys.platform == "darwin":
        try:
            res = subprocess.run(
                [
                    "/usr/bin/security",
                    "find-generic-password",
                    "-s",
                    service,
                    "-a",
                    key,
                    "-w",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            val = res.stdout.rstrip("\r\n")
            return val or None
        except Exception:
            return None

    try:
        res = subprocess.run(
            ["secret-tool", "lookup", "service", service, "account", key],
            check=True,
            capture_output=True,
            text=True,
        )
        val = res.stdout.rstrip("\r\n")
        return val or None
    except Exception:
        return None


def delete_secret(key: str, *, service: str = SERVICE_NAME) -> bool:  # noqa: C901
    """Remove a secret from the OS credential manager."""
    removed = False
    try:
        import keyring  # type: ignore[import-not-found]

        keyring.delete_password(service, key)
        removed = True
    except Exception:
        pass

    if os.name == "nt":
        try:
            import win32cred

            win32cred.CredDelete(f"{service}:{key}", win32cred.CRED_TYPE_GENERIC, 0)
            return True
        except Exception:
            return removed

    if sys.platform == "darwin":
        try:
            subprocess.run(
                [
                    "/usr/bin/security",
                    "delete-generic-password",
                    "-s",
                    service,
                    "-a",
                    key,
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return removed

    try:
        subprocess.run(
            ["secret-tool", "clear", "service", service, "account", key],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return removed


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
    """Loads the configuration from the config file and OS credential store."""
    config_path = get_config_path()
    if config_path.is_symlink():
        raise OSError("CLI credential file must not be a symbolic link")
    data: Dict[str, Any] = {}
    if config_path.exists():
        protect_config(config_path)
        try:
            with config_path.open(encoding="utf-8") as handle:
                loaded = json.load(handle)
                if isinstance(loaded, dict):
                    data = loaded
        except (OSError, ValueError):
            data = {}
    if _os_secret_store_enabled(config_path):
        for secret_key in SECRET_KEYS:
            secret_value = read_secret(secret_key)
            if secret_value is not None:
                data[secret_key] = secret_value
                data["credential_store"] = "os"
    return data


def save_config(config: Dict[str, Any]):
    """Atomically save configuration with owner-only permissions and OS secret store."""
    import tempfile

    config_path = get_config_path()
    if config_path.is_symlink():
        raise OSError("CLI credential file must not be a symbolic link")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    disk_config = dict(config)
    if _os_secret_store_enabled(config_path):
        stored_in_os = False
        for secret_key in SECRET_KEYS:
            value = disk_config.get(secret_key)
            if value is None:
                delete_secret(secret_key)
            elif isinstance(value, str) and write_secret(secret_key, value):
                disk_config[secret_key] = None
                stored_in_os = True
        if stored_in_os:
            disk_config["credential_store"] = "os"
            config["credential_store"] = "os"
        elif any(isinstance(disk_config.get(k), str) for k in SECRET_KEYS):
            disk_config["credential_store"] = "file"
            config["credential_store"] = "file"
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
            json.dump(disk_config, handle, indent=4)
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
    def credential_store(self) -> str:
        """Where sensitive credentials are currently persisted."""
        if os.environ.get("BSM_JWT_TOKEN"):
            return "env"
        store = self._config.get("credential_store")
        if store in {"os", "file"}:
            return str(store)
        return "os" if _os_secret_store_enabled() else "file"

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
