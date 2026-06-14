"""
Link selector popup for markdown links.
"""

from __future__ import annotations

from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import ListItem, ListView, Static

from core.markdown_utils import MarkdownLink


class LinkItem(ListItem):
    """List item representing a markdown link."""

    def __init__(self, link: MarkdownLink):
        super().__init__(Static(f"{link.label} → {link.target}"))
        self.link = link


class LinkSelectorScreen(ModalScreen[MarkdownLink]):
    """
    Modal popup to select a link (centered window, not full screen).
    """

    def __init__(self, links: list[MarkdownLink]):
        super().__init__()
        self._links = links

    def compose(self):
        with Container(id="link-popup", classes="popup-window"):
            yield Static("Select a link:", id="link-title")
            yield ListView(id="link-list")

    def on_mount(self) -> None:
        lv = self.query_one("#link-list", ListView)
        for link in self._links:
            lv.append(LinkItem(link))
        if lv.children:
            lv.index = 0
        lv.focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, LinkItem):
            self.dismiss(item.link)
