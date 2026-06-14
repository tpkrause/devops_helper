"""
Custom plugin: Kubernetes Deployment Runner
"""

from __future__ import annotations
import subprocess

from typing import Any, Dict
from core.plugins import BasePlugin, PluginResult, PluginContext, PluginMetadata
from rich.panel import Panel


class K8sDeployPlugin(BasePlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="K8s Deploy",
            identifier="k8s_deploy",
            description="Run the Kubernetes deployment script.",
        )

    def default_arguments(self) -> Dict[str, Any]:
        return {
            "command": "./scripts/deploy_k8s.sh",
            "namespace": "default",
        }

    def run(self, context: PluginContext, **kwargs: Any) -> PluginResult:
        command = kwargs.get("command")
        namespace = kwargs.get("namespace")

        full_cmd = f"{command} --namespace {namespace}"

        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                cwd=context.working_directory,
                capture_output=True,
                text=True,
            )
        except Exception as exc:
            return PluginResult(Panel(f"Error executing deployment: {exc}"), [])

        output = [f"$ {full_cmd}\n"]
        if result.stdout:
            output.append(result.stdout)
        if result.stderr:
            output.append("\n[stderr]\n" + result.stderr)

        return PluginResult(Panel("".join(output)), [])
