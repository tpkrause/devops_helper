"""
Custom plugin: Version Check
"""

from __future__ import annotations
from typing import Any, Dict
from core.plugins import BasePlugin, PluginContext, PluginMetadata
import subprocess


class VersionCheckPlugin(BasePlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Version Check",
            identifier="version_check",
            description="Run a Python version check script.",
        )

    def default_arguments(self) -> Dict[str, Any]:
        return {"script_path": "scripts/show_version.py"}

    def run(self, context: PluginContext, **kwargs: Any) -> str:
        script_path = kwargs.get("script_path")

        try:
            result = subprocess.run(
                ["python3", script_path],
                cwd=context.working_directory,
                capture_output=True,
                text=True,
            )
        except Exception as exc:
            return f"Error executing version script: {exc}"

        output = [f"$ python3 {script_path}\n"]
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append("\n[stderr]\n" + result.stderr)

        return "".join(output)
