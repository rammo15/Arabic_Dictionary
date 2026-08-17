# arabic-dictionary

A modern, open-source Arabic dictionary toolkit for Python.

```python
from arabic_dictionary.application.dictionary import Dictionary
from arabic_dictionary.providers import WiktionaryProvider
from arabic_dictionary.repository import InMemoryRepository

d = Dictionary(
    repository=InMemoryRepository(),
    provider=WiktionaryProvider(),
)

entry = d.lookup("كتاب")
print(entry.root)                   # كتب
print(entry.plural)                 # كتب
print(entry.senses[0].meaning)
```

## Features

- Look up Arabic words from [Arabic Wiktionary](https://ar.wiktionary.org) with automatic parsing
- Load a local word list from a JSON file using `StaticProvider`
- Combine multiple providers with `CompositeProvider` (first-match, with fallback)
- Cache looked-up entries automatically in a repository (in-memory or SQLite)
- Extract root, plural, word type, examples, synonyms, and antonyms
- Normalize Arabic text (diacritics, alef variants, tā' marbūṭa, etc.)
- Supports both legacy and modern Arabic Wiktionary page formats

## Installation

Requires Python 3.11+.

```bash
pip install arabic-dictionary
```

To install from source:

```bash
git clone https://github.com/rammo15/Arabic_Dictionary.git
cd Arabic_Dictionary
pip install -e ".[dev]"
```

## Quick Start

### Online lookup via Wiktionary

```python
from arabic_dictionary.application.dictionary import Dictionary
from arabic_dictionary.providers import WiktionaryProvider
from arabic_dictionary.repository import InMemoryRepository

d = Dictionary(
    repository=InMemoryRepository(),
    provider=WiktionaryProvider(),
)

entry = d.lookup("كتاب")

if entry:
    print(entry.text)               # كتاب
    print(entry.root)               # كتب
    print(entry.plural)             # كتب
    for sense in entry.senses:
        print(sense.word_type)      # WordType.NOUN
        print(sense.meaning)
        print(sense.examples)
        print(sense.synonyms)
        print(sense.antonyms)
```

The first call fetches the entry from Wiktionary and saves it to the repository.
Subsequent calls for the same word are served from the repository (cache-aside).

### Offline lookup from a JSON file

Prepare a JSON file (`words.json`):

```json
{
  "كتاب": {
    "root": "كتب",
    "plural": "كتب",
    "senses": [
      {
        "meaning": "وعاء للمعرفة يُقرأ.",
        "word_type": "noun",
        "examples": ["هذا كتاب مفيد."],
        "synonyms": ["سِفر"],
        "antonyms": []
      }
    ]
  }
}
```

```python
from arabic_dictionary.providers import StaticProvider

provider = StaticProvider.from_file("words.json")
entry = provider.lookup("كتاب")
```

### Combining providers

Use `CompositeProvider` to try providers in order, returning the first match:

```python
from arabic_dictionary.application.dictionary import Dictionary
from arabic_dictionary.providers import CompositeProvider, StaticProvider, WiktionaryProvider
from arabic_dictionary.repository import InMemoryRepository

provider = CompositeProvider([
    StaticProvider.from_file("custom.json"),  # checked first
    WiktionaryProvider(),                     # fallback
])

d = Dictionary(
    repository=InMemoryRepository(),
    provider=provider,
)

entry = d.lookup("كتاب")
```

## Architecture

```
            Dictionary
                 │
        ┌────────┴────────┐
        │                 │
 Repository (cache)   Provider
        │                 │
      SQLite /        CompositeProvider
      InMemory          ├── StaticProvider
                        └── WiktionaryProvider
```

`Dictionary` is the main entry point. It owns a `Repository` for caching and an
optional `Provider` for live lookups. The `Provider` layer is composable and
independent — advanced users can inject any combination without touching `Dictionary`.

### Domain model

| Class      | Description                                      |
|------------|--------------------------------------------------|
| `Entry`    | A single dictionary word with all its metadata   |
| `Sense`    | One meaning of a word                            |
| `WordType` | Grammatical category (`NOUN`, `VERB`, …)         |

### Providers

| Provider             | Source                       |
|----------------------|------------------------------|
| `WiktionaryProvider` | Arabic Wiktionary (online)   |
| `StaticProvider`     | Local JSON file (offline)    |
| `CompositeProvider`  | Ordered list of providers    |

### Repositories

| Repository           | Description                  |
|----------------------|------------------------------|
| `InMemoryRepository` | In-memory dict (tests / dev) |
| `SQLiteRepository`   | Persistent SQLite database   |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests including live network calls
pytest --run-network

# Lint
ruff check .

# Type check
mypy src/arabic_dictionary/domain tests
```

## License

MIT
