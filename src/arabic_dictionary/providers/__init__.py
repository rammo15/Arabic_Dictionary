from .base import Provider
from .composite import CompositeProvider
from .static import StaticProvider
from .wiktionary import WiktionaryProvider

__all__ = [
    "CompositeProvider",
    "Provider",
    "StaticProvider",
    "WiktionaryProvider",
]