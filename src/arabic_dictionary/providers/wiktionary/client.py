from __future__ import annotations

import requests
from typing import Any

from typing import Any


class MediaWikiClient:
    """Simple client for the MediaWiki API."""

    API_URL = "https://ar.wiktionary.org/w/api.php"

    def get_page(self, title: str) -> dict[str, Any]:
        response = requests.get(
            self.API_URL,
            params={
                "action": "parse",
                "page": title,
                "prop": "wikitext",
                "format": "json",
            },
            timeout=30,
        )

        response.raise_for_status()

        return dict(response.json())
