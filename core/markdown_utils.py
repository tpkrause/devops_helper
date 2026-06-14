"""
Markdown utilities with link extraction and simple plugin:// URL parsing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs

from rich.markdown import Markdown

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


@dataclass
class MarkdownLink:
    label: str
    target: str


def extract_links(markdown_text: str) -> List[MarkdownLink]:
    links: List[MarkdownLink] = []
    for match in LINK_PATTERN.finditer(markdown_text):
        label, target = match.groups()
        links.append(MarkdownLink(label=label, target=target))
    return links


def render_markdown(markdown_text: str) -> Markdown:
    return Markdown(markdown_text, code_theme="monokai", hyperlinks=True)


def parse_plugin_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parse plugin:// URLs like:
      plugin://python_runner?code=print("hi")
      plugin://bash_runner?command=ls -la
      plugin://markdown_docs?file_path=docs/intro.md
    """
    if not url.startswith("plugin://"):
        return None

    parsed = urlparse(url)
    plugin_id = parsed.netloc or parsed.path.lstrip("/")
    params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

    return {"plugin_id": plugin_id, **params}
