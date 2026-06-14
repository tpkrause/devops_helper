"""
Bash/shell script runner plugin.

This plugin executes shell commands and returns their output.
"""

from __future__ import annotations

import subprocess
from typing import Any, Dict

from core.plugins import BasePlugin, PluginContext, PluginMetadata


class BashRunnerPlugin(BasePlugin):
    """
    Plugin that runs shell commands using the system shell.

    This is intended for quick DevOps tasks such as invoking scripts,
    checking service status, or running ad-hoc commands.
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Return metadata describing this plugin."""
        return PluginMetadata(
            name="Bash Runner",
            identifier="bash_runner",
            description="Execute shell commands and scripts.",
        )

    def default_arguments(self) -> Dict[str, Any]:
        """
        Provide default arguments for the plugin.

        Returns
        -------
        dict
            Default command to run.
        """
        return {"command": "echo 'No command specified.'"}

    def run(self, context: PluginContext, **kwargs: Any) -> str:
        """
        Execute a shell command.

        Parameters
        ----------
        context:
            The plugin execution context.
        kwargs:
            Expected to contain a `command` string.

        Returns
        -------
        str
            Combined stdout and stderr from the command.
        """
        command = kwargs.get("command") or self.default_arguments()["command"]
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=context.working_directory,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:  # pragma: no cover - defensive
            return f"Error executing command: {exc}"

        output = []
        output.append(f"$ {command}")
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append("\n[stderr]\n")
            output.append(result.stderr)
        return "".join(output)
