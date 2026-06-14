"""
Documentation browser tree widget.
"""

from __future__ import annotations

from pathlib import Path

from textual.widgets import Tree


class DocBrowser(Tree):
    """
    Tree-based documentation browser compatible with modern Textual.
    """

    def __init__(self, root_path: Path, **kwargs):
        super().__init__("Documentation", **kwargs)
        self.root_path = root_path

    def on_mount(self) -> None:
        self._populate(self.root, self.root_path)

    def _populate(self, node: Tree.Node, path: Path) -> None:
        if not path.exists():
            return
        for child in sorted(path.iterdir()):
            if child.is_dir():
                new_node = node.add(child.name, expand=False)
                self._populate(new_node, child)
            elif child.suffix.lower() == ".md":
                node.add_leaf(child.name, data=str(child))
