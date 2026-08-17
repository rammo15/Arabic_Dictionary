"""
Layered lookup using CompositeProvider.

Checks a local static word list first, then falls back to Wiktionary
for words that are not found locally. The Dictionary caches every
result so each word is only fetched once per session.

Run:
    python examples/composite_provider.py
"""

import json
import tempfile
from pathlib import Path

from arabic_dictionary.application.dictionary import Dictionary
from arabic_dictionary.providers import (
    CompositeProvider,
    StaticProvider,
    WiktionaryProvider,
)
from arabic_dictionary.repository import InMemoryRepository

# Local overrides — these take priority over Wiktionary
local_words = {
    "كتاب": {
        "root": "كتب",
        "plural": "كتب",
        "senses": [{"meaning": "تعريف مخصص للكتاب.", "word_type": "noun"}],
    }
}

with tempfile.NamedTemporaryFile(
    mode="w", suffix=".json", delete=False, encoding="utf-8"
) as f:
    json.dump(local_words, f, ensure_ascii=False)
    local_path = Path(f.name)

provider = CompositeProvider([
    StaticProvider.from_file(local_path),   # checked first (offline)
    WiktionaryProvider(),                    # fallback (online)
])

d = Dictionary(
    repository=InMemoryRepository(),
    provider=provider,
)

# "كتاب" will be served from the static file
entry = d.lookup("كتاب")
if entry:
    print(f"كتاب — source: {entry.source}")
    print(f"       meaning: {entry.senses[0].meaning}")

print()

# "قلم" is not in the local file, so Wiktionary will be consulted
entry = d.lookup("قلم")
if entry:
    print(f"قلم — source: {entry.source}")
    print(f"      meaning: {entry.senses[0].meaning}")
