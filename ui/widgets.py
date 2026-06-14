"""
Common UI widgets for DevOps Helper.
"""

from __future__ import annotations

from rich.text import Text
from textual.widgets import ListItem, Static
from textual.containers import Vertical


class PluginListItem(ListItem):
    """List item representing a plugin in the plugin list."""

    def __init__(self, label: str, plugin_id: str) -> None:
        super().__init__(Static(label))
        self.plugin_id = plugin_id


class DescriptionBar(Static):
    """Top description bar for the selected plugin."""

    def update_description(self, text: str) -> None:
        self.update(text)


class BreadcrumbBar(Static):
    """Breadcrumb bar showing navigation trail."""

    def update_breadcrumb(self, text: str) -> None:
        if text:
            self.update(Text(text, style="bold magenta"))
        else:
            self.update("")


class OutputPanel(Vertical):
    def compose(self):
        # A dedicated container for the markdown content
        yield Static(id="output-content")

    def show_output(self, renderable) -> None:
        content = self.query_one("#output-content", Static)
        content.update(renderable)
