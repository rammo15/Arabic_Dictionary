"""
Offline lookup using StaticProvider.

Loads a word list from a local JSON file and looks up words without any
network access. Useful for bundling a curated word list with your app.

Run:
    python examples/static_provider.py
"""

import json
import tempfile
from pathlib import Path

from arabic_dictionary.providers import StaticProvider

# Build a small in-memory word list for the demo
words = {
    "كتاب": {
        "root": "كتب",
        "plural": "كتب",
        "senses": [
            {
                "meaning": "وعاء للمعرفة يُقرأ.",
                "word_type": "noun",
                "examples": ["هذا كتاب مفيد."],
                "synonyms": ["سِفر"],
                "antonyms": [],
            }
        ],
    },
    "قلم": {
        "senses": [
            {
                "meaning": "أداة للكتابة.",
                "word_type": "noun",
            }
        ],
    },
}

# Write to a temporary file (in real usage, provide your own JSON file)
with tempfile.NamedTemporaryFile(
    mode="w", suffix=".json", delete=False, encoding="utf-8"
) as f:
    json.dump(words, f, ensure_ascii=False)
    path = Path(f.name)

provider = StaticProvider.from_file(path)

for word in ["كتاب", "قلم", "شجرة"]:
    entry = provider.lookup(word)
    if entry is None:
        print(f"{word}: not found")
    else:
        print(f"{word}: {entry.senses[0].meaning}")
