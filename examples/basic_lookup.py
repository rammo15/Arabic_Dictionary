"""
Basic lookup using WiktionaryProvider.

Looks up a word from Arabic Wiktionary and prints all available fields.
The result is cached in the in-memory repository, so subsequent calls
for the same word do not hit the network.

Run:
    python examples/basic_lookup.py
"""

from arabic_dictionary.application.dictionary import Dictionary
from arabic_dictionary.providers import WiktionaryProvider
from arabic_dictionary.repository import InMemoryRepository

d = Dictionary(
    repository=InMemoryRepository(),
    provider=WiktionaryProvider(),
)

entry = d.lookup("كتاب")

if entry is None:
    print("Word not found.")
else:
    print(f"text:   {entry.text}")
    print(f"root:   {entry.root}")
    print(f"plural: {entry.plural}")
    print(f"source: {entry.source}")
    print()
    for i, sense in enumerate(entry.senses, 1):
        print(f"Sense {i}:")
        print(f"  meaning:   {sense.meaning}")
        print(f"  word_type: {sense.word_type}")
        print(f"  examples:  {sense.examples}")
        print(f"  synonyms:  {sense.synonyms}")
        print(f"  antonyms:  {sense.antonyms}")
