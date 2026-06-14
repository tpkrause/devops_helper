"""
Navigation and breadcrumb utilities for DevOps Helper.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class BreadcrumbTrail:
    """Simple breadcrumb trail with push/pop semantics."""

    items: List[str] = field(default_factory=list)

    def push(self, label: str) -> None:
        self.items.append(label)

    def pop(self) -> None:
        if self.items:
            self.items.pop()

    def clear(self) -> None:
        self.items.clear()

    def as_text(self) -> str:
        return " > ".join(self.items)


def breadcrumb_for_path(path: str) -> List[str]:
    """Split a filesystem path into breadcrumb components."""
    return list(Path(path).parts)
