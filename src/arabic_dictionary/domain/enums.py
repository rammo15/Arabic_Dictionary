from enum import Enum


class WordType(str, Enum):
    """أنواع الكلمات."""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PARTICLE = "particle"
    PHRASE = "phrase"
    UNKNOWN = "unknown"


class RelationType(str, Enum):
    """العلاقات بين الكلمات."""

    SYNONYM = "synonym"
    ANTONYM = "antonym"
    DERIVED = "derived"
    RELATED = "related"
    PLURAL = "plural"
    SINGULAR = "singular"
    FEMININE = "feminine"
    MASCULINE = "masculine"
