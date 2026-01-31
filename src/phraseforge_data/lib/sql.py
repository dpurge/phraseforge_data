CREATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS phrase (
    id VARCHAR PRIMARY KEY,
    text VARCHAR NOT NULL,
    grammar VARCHAR,
    transcription VARCHAR,
    created TIMESTAMP NOT NULL,
);

CREATE TABLE IF NOT EXISTS phrase_translation_{translation_language}_{translation_script} (
    id VARCHAR PRIMARY KEY,
    text VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL,
);

CREATE TABLE IF NOT EXISTS phrase_to_translation_{translation_language}_{translation_script} (
    phrase_id VARCHAR NOT NULL,
    translation_id VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL,
    PRIMARY KEY (phrase_id, translation_id),
    FOREIGN KEY (phrase_id) REFERENCES phrase (id),
    FOREIGN KEY (translation_id) REFERENCES phrase_translation_{translation_language}_{translation_script} (id),
);

CREATE TABLE IF NOT EXISTS phrase_note_{translation_language}_{translation_script} (
    id VARCHAR PRIMARY KEY,
    text VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL,
);

CREATE TABLE IF NOT EXISTS phrase_to_note_{translation_language}_{translation_script} (
    phrase_id VARCHAR NOT NULL,
    note_id VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL,
    PRIMARY KEY (phrase_id, note_id),
    FOREIGN KEY (phrase_id) REFERENCES phrase (id),
    FOREIGN KEY (note_id) REFERENCES phrase_note_{translation_language}_{translation_script} (id),
);

CREATE TABLE IF NOT EXISTS document (
    id VARCHAR PRIMARY KEY,
    type VARCHAR NOT NULL,
    document VARCHAR NOT NULL,
    chunk VARCHAR NOT NULL,
    description VARCHAR,
    created TIMESTAMP NOT NULL,
);

CREATE TABLE IF NOT EXISTS document_to_phrase (
    document_id VARCHAR NOT NULL,
    phrase_id VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL,
    PRIMARY KEY (document_id, phrase_id),
    FOREIGN KEY (document_id) REFERENCES document (id),
    FOREIGN KEY (phrase_id) REFERENCES phrase (id),
);
"""

IMPORT_DOCUMENT = "INSERT OR IGNORE INTO document (id, type, document, chunk, description, created) VALUES (?, ?, ?, ?, ?, ?)"

FIND_DOCUMENT = "SELECT id, document, chunk, description, created FROM document WHERE type = ?"

IMPORT_PHRASE = "INSERT OR IGNORE INTO phrase (id, text, grammar, transcription, created) VALUES (?, ?, ?, ?, ?)"

CONNECT_DOCUMENT_TO_PHRASE = "INSERT OR IGNORE INTO document_to_phrase (document_id, phrase_id, created) VALUES (?, ?, ?)"

FIND_PHRASE_FOR_DOCUMENT = "SELECT id, text, grammar, transcription, created FROM phrase WHERE id IN (SELECT phrase_id FROM document_to_phrase WHERE document_id = ?)"

IMPORT_PHRASE_TRANSLATION = "INSERT OR IGNORE INTO phrase_translation_{translation_language}_{translation_script} (id, text, created) VALUES (?, ?, ?)"

CONNECT_PHRASE_TO_TRANSLATION = "INSERT OR IGNORE INTO phrase_to_translation_{translation_language}_{translation_script} (phrase_id, translation_id, created) VALUES (?, ?, ?)"

FIND_TRANSLATION_FOR_PHRASE = "SELECT id, text, created FROM phrase_translation_{translation_language}_{translation_script} WHERE id IN (SELECT translation_id FROM phrase_to_translation_{translation_language}_{translation_script} WHERE phrase_id = ?)"

IMPORT_PHRASE_NOTE = "INSERT OR IGNORE INTO phrase_note_{translation_language}_{translation_script} (id, text, created) VALUES (?, ?, ?)"

CONNECT_PHRASE_TO_NOTE = "INSERT OR IGNORE INTO phrase_to_note_{translation_language}_{translation_script} (phrase_id, note_id, created) VALUES (?, ?, ?)"

FIND_NOTE_FOR_PHRASE = "SELECT id, text, created FROM phrase_note_{translation_language}_{translation_script} WHERE id IN (SELECT note_id FROM phrase_to_note_{translation_language}_{translation_script} WHERE phrase_id = ?)"
