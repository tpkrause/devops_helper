"""
Bash/shell script runner plugin.

This plugin executes shell commands and returns their output.
"""

from __future__ import annotations

import subprocess
from typing import Any, Dict
from rich.panel import Panel

from core.plugins import BasePlugin, PluginContext, PluginMetadata
from core.plugins import PluginResult


class BashRunnerPlugin(BasePlugin):
    """
    Plugin that runs shell commands using the system shell.

    This is intended for quick DevOps tasks such as invoking scripts,
    checking service status, or running ad-hoc commands.
    """

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Bash Runner",
            identifier="bash_runner",
            description="Execute shell commands and scripts.",
        )

    def default_arguments(self) -> Dict[str, Any]:
        return {"command": "echo 'No command specified.'"}

    def run(self, context: PluginContext, **kwargs: Any) -> PluginResult:
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
            return PluginResult(
                renderable=Panel(
                    f"Error executing command: {exc}",
                    title="Bash Output",
                    border_style="red",
                ),
                links=[],
            )

        output = []
        output.append(f"$ {command}")
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append("\n[stderr]\n")
            output.append(result.stderr)
        return PluginResult(
            renderable=Panel(
                "".join(output), title="Bash Output", border_style="green"
            ),
            links=[],
        )
