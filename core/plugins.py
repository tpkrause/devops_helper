"""
Core plugin abstractions for the DevOps helper TUI.

This module defines the base plugin protocol and common data structures
used by all plugins.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, List
from rich.console import RenderableType


@dataclass
class PluginResult:
    renderable: RenderableType
    links: List[Any]


@dataclass
class PluginMetadata:
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
        self.working_directory = working_directory or "."


class BasePlugin(ABC):
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        raise NotImplementedError

    @abstractmethod
    def run(self, context: PluginContext, **kwargs) -> PluginResult:
        raise NotImplementedError

    def default_arguments(self) -> Dict[str, Any]:
        return {}
