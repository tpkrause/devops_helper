"""
MarkdownDocsPlugin — Markdown file / content viewer for Textual 0.8.x

This plugin:
- Loads a .md file from disk OR renders provided markdown content
- Renders it using Rich Markdown
- Extracts links (http, https, plugin://, and local .md)
- Returns (renderable, links) to the app
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from rich.markdown import Markdown
from rich.panel import Panel

from core.plugins import BasePlugin, PluginMetadata, PluginContext


# ------------------------------------------------------------
# Data structure for extracted links
# ------------------------------------------------------------


@dataclass
class MarkdownLink:
    label: str
    target: str


# ------------------------------------------------------------
# Link extraction
# ------------------------------------------------------------

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def extract_links(markdown_text: str) -> List[MarkdownLink]:
    """Extract all markdown links from the text."""
    links: List[MarkdownLink] = []
    for match in LINK_PATTERN.finditer(markdown_text):
        label, target = match.groups()
        links.append(MarkdownLink(label=label, target=target))
    return links


# ------------------------------------------------------------
# Plugin implementation
# ------------------------------------------------------------


class MarkdownDocsPlugin(BasePlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="markdown_docs",
            name="Markdown Docs Viewer",
            description="View Markdown documentation files or inline markdown content.",
        )

    def default_arguments(self) -> dict:
        # Default to a docs entry point; content is optional and overrides file_path
        return {
            "file_path": "docs/intro.md",
            "content": None,
        }

    # --------------------------------------------------------
    # Main plugin entry point
    # --------------------------------------------------------

    def run(
        self,
        context: PluginContext,
        file_path: Optional[str] = None,
        content: Optional[str] = None,
        **_: object,
    ) -> Tuple[Panel, List[MarkdownLink]]:
        """
        Render markdown from either a file or direct content.

        Precedence:
        - If `content` is provided, render that.
        - Else if `file_path` is provided, load and render the file.
        """

        # Decide source of markdown text
        if content is not None:
            text = content
            title = "Inline Markdown"
        else:
            if not file_path:
                return (
                    Panel(
                        "[red]No file_path or content provided to markdown_docs.[/red]"
                    ),
                    [],
                )

            path = Path(file_path)

            if not path.exists():
                return (
                    Panel(f"[red]File not found:[/red] {file_path}"),
                    [],
                )

            text = path.read_text(encoding="utf-8")
            title = str(path)

        # Extract links
        links = extract_links(text)

        # Render markdown (Rich handles formatting)
        md = Markdown(text, hyperlinks=True)

        # Wrap in a Panel for nicer display
        panel = Panel(
            md,
            title=title,
            border_style="cyan",
            expand=True,
        )

        return panel, links
