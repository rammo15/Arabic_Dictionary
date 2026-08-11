from .providers import Provider
from .storage import SQLiteStorage


class SQLiteProvider(Provider):

    name = "SQLite"

    def __init__(self, storage: SQLiteStorage):

        self.storage = storage

    def lookup(self, word):

        return self.storage.get(word)
