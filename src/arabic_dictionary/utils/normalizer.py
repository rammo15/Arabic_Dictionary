from __future__ import annotations

import re

_DIACRITICS = re.compile(
    r"[\u064B-\u065F\u0670\u06D6-\u06ED]"
)


def normalize(text: str) -> str:
    """Normalize Arabic text for indexing and searching."""

    text = text.strip()

    # Remove tatweel
    text = text.replace("ـ", "")

    # Normalize alef
    text = (
        text.replace("أ", "ا")
            .replace("إ", "ا")
            .replace("آ", "ا")
    )

    # Normalize ya
    text = text.replace("ى", "ي")

    # Normalize ta marbuta
    text = text.replace("ة", "ه")

    # Remove diacritics
    text = _DIACRITICS.sub("", text)

    return text