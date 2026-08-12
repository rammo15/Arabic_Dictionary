"""
Enumerations used across the domain layer.
"""

from __future__ import annotations

from enum import Enum


class WordType(str, Enum):
    """Represents the grammatical category of a word."""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PARTICLE = "particle"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    PHRASE = "phrase"
    UNKNOWN = "unknown"


class RelationType(str, Enum):
    """Represents semantic relationships between words."""

    SYNONYM = "synonym"
    ANTONYM = "antonym"
    RELATED = "related"
    DERIVED = "derived"
    PLURAL = "plural"
    SINGULAR = "singular"
    FEMININE = "feminine"
    MASCULINE = "masculine"
