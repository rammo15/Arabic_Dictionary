from __future__ import annotations

import re

_DIACRITICS = re.compile(
    r"[\u064B-\u065F\u0670\u06D6-\u06ED]"
)


def strip_diacritics(text: str) -> str:
    """Remove diacritics and tatweel only, preserving all letter forms.

    Use this before an API lookup so that قَلَمٌ → قلم and كـتاب → كتاب,
    without altering letters like ة, أ, ى that carry meaning.
    """
    text = text.strip()
    text = text.replace("ـ", "")
    text = _DIACRITICS.sub("", text)
    return text


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