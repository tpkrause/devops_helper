"""
Persistent configuration system for DevOps Helper.

Stores per-plugin configuration in:
    ~/.devops_helper/config.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


CONFIG_PATH = Path.home() / ".devops_helper" / "config.json"


class ConfigManager:
    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if CONFIG_PATH.exists():
            try:
                self._data = json.loads(CONFIG_PATH.read_text())
            except Exception:
                self._data = {}
        else:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            self._save()

    def _save(self) -> None:
        CONFIG_PATH.write_text(json.dumps(self._data, indent=2))

    def get_plugin_config(self, plugin_id: str) -> Dict[str, Any]:
        return self._data.setdefault(plugin_id, {})

    def update_plugin_config(self, plugin_id: str, updates: Dict[str, Any]) -> None:
        section = self._data.setdefault(plugin_id, {})
        section.update(updates)
        self._save()
