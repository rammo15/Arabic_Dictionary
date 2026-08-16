from __future__ import annotations

from typing import Any

import requests


class MediaWikiClient:
    """Simple client for the MediaWiki API."""

    API_URL = "https://ar.wiktionary.org/w/api.php"
    USER_AGENT = "ArabicDictionary/0.1 (github.com/rammo15/Arabic_Dictionary)"

    def get_page(self, title: str) -> dict[str, Any]:
        response = requests.get(
            self.API_URL,
            params={
                "action": "parse",
                "page": title,
                "prop": "wikitext",
                "format": "json",
                "redirects": "1",
            },
            headers={"User-Agent": self.USER_AGENT},
            timeout=30,
        )

        response.raise_for_status()

        return dict(response.json())
