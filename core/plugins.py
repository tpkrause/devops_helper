"""
Core plugin abstractions for the DevOps helper TUI.

This module defines the base plugin protocol and common data structures
used by all plugins.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PluginMetadata:
    """
    Metadata describing a plugin.

    Attributes
    ----------
    name:
        Human-readable name of the plugin.
    identifier:
        Unique identifier used internally and in the registry.
    description:
        Short description shown in the top bar when selected.
    """

    name: str
    identifier: str
    description: str


class PluginContext:
    """
    Context object passed to plugins when they are executed.

    This can be extended to include configuration, environment variables,
    logging hooks, or other shared resources.
    """

    def __init__(self, working_directory: Optional[str] = None) -> None:
        """
        Initialize a new plugin context.

        Parameters
        ----------
        working_directory:
            Optional working directory for plugin execution.
        """
        self.working_directory = working_directory or "."


class BasePlugin(ABC):
    """
    Abstract base class for all plugins.

    Plugins must provide metadata and implement the `run` method.
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        raise NotImplementedError

    @abstractmethod
    def run(self, context: PluginContext, **kwargs: Any) -> str:
        raise NotImplementedError

    def default_arguments(self) -> Dict[str, Any]:
        return {}
