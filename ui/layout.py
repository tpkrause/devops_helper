"""
Layout helpers for DevOps Helper Textual app.
"""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, ListView

from ui.widgets import BreadcrumbBar, DescriptionBar, OutputPanel
from ui.doc_browser import DocBrowser


def build_main_layout(docs_root: Path) -> ComposeResult:
    """
    Build the main application layout.

    Yields
    ------
    ComposeResult
        The composed widgets.
    """
    yield Header()
    yield BreadcrumbBar(id="breadcrumb-bar")
    yield DescriptionBar(id="description-bar")

    with Container(id="main-container"):
        with Horizontal():
            with Vertical(id="left-pane"):
                yield ListView(id="plugin-list")
                yield DocBrowser(docs_root, id="doc-browser")
            yield OutputPanel(id="output-panel")

    yield Footer()
