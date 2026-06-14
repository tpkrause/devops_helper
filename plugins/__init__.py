"""
Plugin package for the DevOps helper TUI.

This module exposes all built-in plugins for easy registration.
"""

from __future__ import annotations

from .bash_runner import BashRunnerPlugin
from .python_runner import PythonRunnerPlugin
from .markdown_docs import MarkdownDocsPlugin
from .custom_k8s_deploy import K8sDeployPlugin
from .custom_version_check import VersionCheckPlugin

BUILTIN_PLUGINS = [
    BashRunnerPlugin,
    PythonRunnerPlugin,
    MarkdownDocsPlugin,
    K8sDeployPlugin,
    VersionCheckPlugin,
]
