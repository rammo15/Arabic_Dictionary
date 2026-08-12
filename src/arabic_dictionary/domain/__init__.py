"""
Domain models and enums.
"""

from .enums import RelationType, WordType
from .models import Entry, Sense

__all__ = [
    "Entry",
    "Sense",
    "RelationType",
    "WordType",
]
