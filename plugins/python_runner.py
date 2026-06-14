"""
Python script runner plugin.

This plugin executes Python code in a subprocess, allowing DevOps
engineers to run small utilities or scripts.
"""

from __future__ import annotations

import subprocess
import sys
from typing import Any, Dict

from core.plugins import BasePlugin, PluginContext, PluginMetadata


class PythonRunnerPlugin(BasePlugin):
    """
    Plugin that runs Python scripts or inline code.

    For safety and clarity, this implementation uses a subprocess
    invocation of the current Python interpreter.
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Return metadata describing this plugin."""
        return PluginMetadata(
            name="Python Runner",
            identifier="python_runner",
            description="Execute Python scripts or inline code.",
        )

    def default_arguments(self) -> Dict[str, Any]:
        """
        Provide default arguments for the plugin.

        Returns
        -------
        dict
            Default Python code to run.
        """
        return {"code": "print('No Python code specified.')"}

    def run(self, context: PluginContext, **kwargs: Any) -> str:
        """
        Execute Python code in a subprocess.

        Parameters
        ----------
        context:
            The plugin execution context.
        kwargs:
            Expected to contain either `code` or `script_path`.

        Returns
        -------
        str
            Combined stdout and stderr from the Python execution.
        """
        code = kwargs.get("code")
        script_path = kwargs.get("script_path")

        if script_path:
            cmd = [sys.executable, script_path]
            display = f"python {script_path}"
        else:
            if not code:
                code = self.default_arguments()["code"]
            cmd = [sys.executable, "-c", code]
            display = f"python -c {code!r}"

        try:
            result = subprocess.run(
                cmd,
                cwd=context.working_directory,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:  # pragma: no cover - defensive
            return f"Error executing Python: {exc}"

        output = []
        output.append(f"$ {display}\n")
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append("\n[stderr]\n")
            output.append(result.stderr)
        return "".join(output)
