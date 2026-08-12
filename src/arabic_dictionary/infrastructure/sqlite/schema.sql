PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    text TEXT NOT NULL UNIQUE,
    normalized_text TEXT NOT NULL,

    root TEXT,
    pronunciation TEXT,
    etymology TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS senses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    entry_id INTEGER NOT NULL,

    meaning TEXT NOT NULL,

    word_type TEXT,

    notes TEXT,

    FOREIGN KEY(entry_id)
        REFERENCES entries(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sense_id INTEGER NOT NULL,

    text TEXT NOT NULL,

    source TEXT,

    FOREIGN KEY(sense_id)
        REFERENCES senses(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    sense_id INTEGER NOT NULL,

    word TEXT NOT NULL,

    relation_type TEXT NOT NULL,

    FOREIGN KEY(sense_id)
        REFERENCES senses(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_entries_text
ON entries(text);

CREATE INDEX IF NOT EXISTS idx_entries_normalized
ON entries(normalized_text);