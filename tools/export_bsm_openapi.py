"""Export OpenAPI JSON from the installed Bedrock Server Manager package."""

from __future__ import annotations

import argparse
import asyncio
import json
import tempfile
from pathlib import Path


async def export_schema(output: Path) -> None:
    """Create an isolated BSM app and export its FastAPI OpenAPI document."""
    from bedrock_server_manager.config import bcm_config
    from bedrock_server_manager.context import AppContext
    from bedrock_server_manager.db.database import Database
    from bedrock_server_manager.db.models import Base
    from bedrock_server_manager.db.storage import Storage
    from bedrock_server_manager.state.app_state import AppState
    from bedrock_server_manager.utils.general import startup_checks
    from bedrock_server_manager.web.app import create_web_app

    with tempfile.TemporaryDirectory(prefix="bsm-openapi-export-") as tmp:
        root = Path(tmp)
        data_dir = root / "data"
        config_dir = root / "config"
        plugins_dir = root / "plugins"
        data_dir.mkdir()
        config_dir.mkdir()
        plugins_dir.mkdir()

        db_path = data_dir / "bsm.db"
        config_path = config_dir / "bedrock_server_manager.json"
        config_path.write_text(
            json.dumps(
                {
                    "data_dir": str(data_dir),
                    "db_url": f"sqlite:///{db_path}",
                    "log_level": "WARNING",
                }
            ),
            encoding="utf-8",
        )

        bcm_config.set_custom_config_dir(str(config_dir))
        bcm_config.set_custom_data_dir(str(data_dir))
        database = Database(f"sqlite+aiosqlite:///{db_path}")
        database.initialize()

        try:
            if database.engine is None:
                raise RuntimeError("BSM database engine was not initialized")
            async with database.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

            storage = Storage(db=database, data_dir=str(data_dir))
            state = AppState()
            await storage.load_state(state)

            context = AppContext()
            context._db = database
            context._storage = storage
            context._state = state
            await context.load()
            startup_checks(context)
            await context.settings.set("paths.plugins", str(plugins_dir))
            context.plugin_manager.plugin_dirs = [plugins_dir]

            app = create_web_app(context)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        finally:
            await database.shutdown()
            bcm_config.set_custom_config_dir(None)
            bcm_config.set_custom_data_dir(None)
            bcm_config.set_custom_db_url(None)
            bcm_config.set_custom_log_level(None)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("openapi.json"),
        help="Destination OpenAPI JSON file",
    )
    args = parser.parse_args()
    asyncio.run(export_schema(args.output))


if __name__ == "__main__":
    main()
