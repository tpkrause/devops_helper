"""
Main Textual TUI application for the DevOps helper.

This file is now thin: it wires together core, plugins, and UI modules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from textual.app import App
from textual.reactive import reactive
from textual.widgets import ListView, Tree

from core.config import ConfigManager
from core.markdown_utils import MarkdownLink, parse_plugin_url
from core.navigation import BreadcrumbTrail, breadcrumb_for_path
from core.plugins import PluginContext, PluginResult
from core.registry import PluginRegistry
from plugins import BUILTIN_PLUGINS
from ui.layout import build_main_layout
from ui.link_popup import LinkSelectorScreen
from ui.widgets import (
    BreadcrumbBar,
    DescriptionBar,
    OutputPanel,
    PluginListItem,
)


class DevOpsHelperApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    #breadcrumb-bar {
        height: 1;
        border: solid gray;
    }

    #description-bar {
        height: 3;
        border: solid gray;
    }

    #main-container {
        height: 1fr;
    }

    #left-pane {
        width: 30%;
        border: solid gray;
    }

    #plugin-list {
        height: 40%;
        border: solid gray;
    }

    #doc-browser {
        height: 60%;
        border: solid gray;
    }

    #output-panel {
        height: 1fr;
        border: solid gray;
        overflow-y: scroll;
    }

    .popup-window {
        width: 60%;
        height: 40%;
        border: solid green;
        background: #202020;
        padding: 1;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("enter", "run_plugin", "Run selected plugin"),
        ("r", "run_plugin", "Run selected plugin"),
        ("l", "open_link_popup", "Open link popup"),
        ("b", "breadcrumb_back", "Breadcrumb back"),
    ]

    selected_plugin_id: reactive[Optional[str]] = reactive(None)

    def __init__(self) -> None:
        super().__init__()
        self.registry = PluginRegistry()
        self.registry.load_from_iterable(BUILTIN_PLUGINS)
        self.config = ConfigManager()
        self.current_links: list[MarkdownLink] = []
        self.breadcrumb = BreadcrumbTrail()

        self._metadata_by_id: Dict[str, str] = {
            meta.identifier: meta.description for meta in self.registry.all_metadata()
        }

    # layout

    def compose(self):
        docs_root = Path("docs")
        yield from build_main_layout(docs_root)

    # lifecycle

    def on_mount(self) -> None:
        plugin_list = self.query_one("#plugin-list", ListView)

        for meta in self.registry.all_metadata():
            plugin_list.append(PluginListItem(meta.name, meta.identifier))

        if plugin_list.children:
            plugin_list.index = 0
            first = plugin_list.children[0]
            if isinstance(first, PluginListItem):
                self.selected_plugin_id = first.plugin_id
                self._update_description_for_selected()

        self._refresh_breadcrumb_bar()

    # helpers

    def _update_description_for_selected(self) -> None:
        desc_bar = self.query_one("#description-bar", DescriptionBar)
        if not self.selected_plugin_id:
            desc_bar.update_description("No plugin selected.")
            return
        desc = self._metadata_by_id.get(self.selected_plugin_id, "")
        desc_bar.update_description(desc)

    def _refresh_breadcrumb_bar(self) -> None:
        bar = self.query_one("#breadcrumb-bar", BreadcrumbBar)
        bar.update_breadcrumb(self.breadcrumb.as_text())

    def _push_path_breadcrumb(self, path: str) -> None:
        self.breadcrumb.clear()
        for part in breadcrumb_for_path(path):
            self.breadcrumb.push(part)
        self._refresh_breadcrumb_bar()

    # events

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        item = event.item
        if isinstance(item, PluginListItem):
            self.selected_plugin_id = item.plugin_id
            self._update_description_for_selected()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        path = event.node.data
        if not path:
            return

        plugin = self.registry.instantiate("markdown_docs")
        context = PluginContext()
        result = plugin.run(context, file_path=path)
        renderable = result.renderable
        self.current_links = result.links

        self.query_one("#output-panel", OutputPanel).show_output(renderable)
        self._push_path_breadcrumb(path)

    # actions

    def action_run_plugin(self) -> None:
        if not self.selected_plugin_id:
            return

        plugin = self.registry.instantiate(self.selected_plugin_id)
        context = PluginContext()

        saved_cfg = self.config.get_plugin_config(plugin.metadata.identifier)
        args = plugin.default_arguments().copy()
        args.update(saved_cfg)

        self.config.update_plugin_config(plugin.metadata.identifier, args)

        result = plugin.run(context, **args)
        renderable = result.renderable
        self.current_links = result.links

        self.query_one("#output-panel", OutputPanel).show_output(renderable)

        self.breadcrumb.clear()
        self.breadcrumb.push(plugin.metadata.name)
        self._refresh_breadcrumb_bar()

    def action_open_link_popup(self) -> None:
        if not self.current_links:
            return

        def _on_dismiss(link: MarkdownLink | None) -> None:
            if link is None:
                return

            parsed = parse_plugin_url(link.target)
            if not parsed:
                return

            plugin_id = parsed.pop("plugin_id", None)
            if not plugin_id:
                return

            plugin = self.registry.instantiate(plugin_id)
            context = PluginContext()
            result = plugin.run(context, **parsed)
            renderable = result.renderable
            self.current_links = result.links

            self.query_one("#output-panel", OutputPanel).show_output(renderable)

            if plugin_id == "markdown_docs" and "file_path" in parsed:
                self._push_path_breadcrumb(parsed["file_path"])
            else:
                self.breadcrumb.clear()
                self.breadcrumb.push(plugin.metadata.name)
                self._refresh_breadcrumb_bar()

        self.push_screen(LinkSelectorScreen(self.current_links), _on_dismiss)

    def action_breadcrumb_back(self) -> None:
        self.breadcrumb.pop()
        self._refresh_breadcrumb_bar()


if __name__ == "__main__":
    app = DevOpsHelperApp()
    app.run()
