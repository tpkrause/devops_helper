"""
Plugin registry for the DevOps helper TUI.

This module provides a simple registry that discovers and stores plugins.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Type

from .plugins import BasePlugin, PluginMetadata


class PluginRegistry:
    """
    Registry for available plugins.

    The registry maintains a mapping from plugin identifiers to plugin
    classes and provides helper methods for discovery and instantiation.
    """

    def __init__(self) -> None:
        """Initialize an empty plugin registry."""
        self._plugins: Dict[str, Type[BasePlugin]] = {}

    def register(self, plugin_cls: Type[BasePlugin]) -> None:
        """
        Register a plugin class.

        Parameters
        ----------
        plugin_cls:
            The plugin class to register. Its `metadata.identifier`
            must be unique.
        """
        identifier = plugin_cls().metadata.identifier
        if identifier in self._plugins:
            raise ValueError(f"Duplicate plugin identifier: {identifier}")
        self._plugins[identifier] = plugin_cls

    def get(self, identifier: str) -> Optional[Type[BasePlugin]]:
        """
        Retrieve a plugin class by identifier.

        Parameters
        ----------
        identifier:
            The plugin identifier.

        Returns
        -------
        Optional[Type[BasePlugin]]
            The plugin class if found, otherwise None.
        """
        return self._plugins.get(identifier)

    def all_metadata(self) -> List[PluginMetadata]:
        """
        Return metadata for all registered plugins.

        Returns
        -------
        list of PluginMetadata
            Metadata objects for all plugins.
        """
        return [cls().metadata for cls in self._plugins.values()]

    def instantiate(self, identifier: str) -> BasePlugin:
        """
        Instantiate a plugin by identifier.

        Parameters
        ----------
        identifier:
            The plugin identifier.

        Returns
        -------
        BasePlugin
            An instance of the requested plugin.

        Raises
        ------
        KeyError
            If the identifier is not registered.
        """
        plugin_cls = self._plugins.get(identifier)
        if plugin_cls is None:
            raise KeyError(f"Plugin not found: {identifier}")
        return plugin_cls()

    def load_from_iterable(self, plugin_classes: Iterable[Type[BasePlugin]]) -> None:
        """
        Bulk-register plugin classes from an iterable.

        Parameters
        ----------
        plugin_classes:
            Iterable of plugin classes to register.
        """
        for cls in plugin_classes:
            self.register(cls)
