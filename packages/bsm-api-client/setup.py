"""Generate the typed client during package builds."""

import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "src" / "bsm_api_client" / "generated" / "openapi.json"
LOCAL_GENERATOR = HERE / "generate_client.py"
REPO_GENERATOR = HERE.parents[1] / "tools" / "generate_client.py"


def generator_path():
    candidate = LOCAL_GENERATOR if LOCAL_GENERATOR.is_file() else REPO_GENERATOR
    if not candidate.is_file():
        raise RuntimeError("Missing OpenAPI client generator.")
    if not SCHEMA.is_file():
        raise RuntimeError("Missing bundled OpenAPI schema.")
    return candidate


class GeneratedBuildPy(build_py):
    def run(self):
        super().run()
        if getattr(self, "editable_mode", False):
            output = SCHEMA.parent
        else:
            output = Path(self.build_lib) / "bsm_api_client" / "generated"
        subprocess.run(
            [
                sys.executable,
                str(generator_path()),
                str(SCHEMA),
                "--output",
                str(output),
            ],
            check=True,
        )
        if getattr(self, "editable_mode", False):
            # Regeneration can replace tag packages discovered when setup began.
            # Both build_py and the subsequent egg_info must use the new tree.
            packages = find_packages(
                where=str(HERE / "src"), include=["bsm_api_client*"]
            )
            self.distribution.packages = packages
            self.packages = packages
            self.__dict__.pop("data_files", None)


class GeneratedSdist(sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)
        generated = Path(base_dir) / "src" / "bsm_api_client" / "generated"
        for item in generated.iterdir():
            if item.name not in {"__init__.py", "openapi.json"}:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        shutil.copyfile(generator_path(), Path(base_dir) / "generate_client.py")


setup(cmdclass={"build_py": GeneratedBuildPy, "sdist": GeneratedSdist})
