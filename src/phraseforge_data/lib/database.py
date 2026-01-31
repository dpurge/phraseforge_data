from datetime import datetime

from typing import (
    Generator,
    Tuple,
)

from duckdb import (
    connect,
)

from ..dat import data_home

from .basetype import (
    DataType,
    Language_and_Script,
    Document,
    Header,
    Vocabulary,
    VocabularyItem,
    Phrase,
    Grammar,
)

from .parser import (
    get_id,
)

from .sql import (
    CREATE_SCHEMA,
    IMPORT_DOCUMENT,
    FIND_DOCUMENT,
    IMPORT_PHRASE,
    CONNECT_DOCUMENT_TO_PHRASE,
    IMPORT_PHRASE_TRANSLATION,
    CONNECT_PHRASE_TO_TRANSLATION,
    IMPORT_PHRASE_NOTE,
    CONNECT_PHRASE_TO_NOTE,
    FIND_PHRASE_FOR_DOCUMENT,
    FIND_TRANSLATION_FOR_PHRASE,
    FIND_NOTE_FOR_PHRASE,
)

class Database:
    def __init__(self, data, translation, **kwargs):
        "Initialize database object to work with module data"

        if not data:
            raise Exception('Database context is missing "data" key')

        if not translation:
            raise Exception('Database context is missing "translation" key')

        self.data_language = data.language.value
        self.data_script = data.script.value
        self.translation_language = translation.language.value
        self.translation_script = translation.script.value

        self.config = {}
        self.connection = None
        self.database = data_home() / f'{self.data_language}-{self.data_script}.duckdb'
        self.sqlparams = {
            'translation_language': self.translation_language,
            'translation_script': self.translation_script,
        }

    def __enter__(self):
        if not self.connection:
            self.connection = connect(self.database)

        self.connection.execute(CREATE_SCHEMA.format(**self.sqlparams))
        
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if self.connection:
            self.connection.close()

    def import_vocabulary(self, document):
        now = datetime.now()
        header = document.header
        document_id = get_id(header.type.value, header.document, header.chunk)

        # print(header)

        self.connection.execute(IMPORT_DOCUMENT.format(**self.sqlparams), [
            document_id,
            header.type.value,
            header.document,
            header.chunk,
            header.description,
            header.created])

        items = document.body.items
        for item in items:
            phrase = item.phrase
            translations = item.translations if item.translations else []
            notes = item.notes if item.notes else []

            phrase_id = get_id(phrase.text, phrase.grammar, phrase.transcription)

            self.connection.execute(IMPORT_PHRASE.format(**self.sqlparams), [
                phrase_id,
                phrase.text,
                phrase.grammar,
                phrase.transcription,
                phrase.created])
            
            self.connection.execute(CONNECT_DOCUMENT_TO_PHRASE.format(**self.sqlparams), [
                document_id,
                phrase_id,
                now])

            for translation in translations:
                translation_id = get_id(translation)

                self.connection.execute(IMPORT_PHRASE_TRANSLATION.format(**self.sqlparams), [
                    translation_id,
                    translation,
                    now])
                
                self.connection.execute(CONNECT_PHRASE_TO_TRANSLATION.format(**self.sqlparams), [
                    phrase_id,
                    translation_id,
                    now])

            for note in notes:
                note_id = get_id(note)

                self.connection.execute(IMPORT_PHRASE_NOTE.format(**self.sqlparams), [
                    note_id,
                    note,
                    now])
                
                self.connection.execute(CONNECT_PHRASE_TO_NOTE.format(**self.sqlparams), [
                    phrase_id,
                    note_id,
                    now])

    def find_document(self, document_type: DataType, document_id: str = None, chunk_id: str = None, items: bool = False) -> Generator[Document]:

        doc_data = self.connection.execute(FIND_DOCUMENT.format(**self.sqlparams), [document_type])
        
        for doc_row in doc_data.fetchall():
            doc_id, document, chunk, description, doc_created = doc_row
            if document_id and not document.startswith(document_id): continue
            if chunk_id and not chunk.startswith(chunk_id): continue

            header = Header(
                document = document,
                chunk = chunk,
                type=document_type,
                description=description,
                data=Language_and_Script(language=self.data_language, script=self.data_script),
                translation=Language_and_Script(language=self.translation_language, script=self.translation_script),
                created=doc_created)
            
            phrases = []
            if items:
                phrase_data = self.connection.execute(FIND_PHRASE_FOR_DOCUMENT.format(**self.sqlparams), [doc_id])
                for phrase_row in phrase_data.fetchall():
                    phrase_id, phrase_text, grammar, transcription, phrase_created = phrase_row
                    phrase_item = Phrase(
                        text = phrase_text,
                        grammar = Grammar(text = grammar) if grammar else None,
                        transcription = transcription,
                        created = phrase_created)
                    
                    translation_data = self.connection.execute(FIND_TRANSLATION_FOR_PHRASE.format(**self.sqlparams), [phrase_id])
                    translation_item = [x[1] for x in translation_data.fetchall()]
                    
                    note_data = self.connection.execute(FIND_NOTE_FOR_PHRASE.format(**self.sqlparams), [phrase_id])
                    note_item = [x[1] for x in note_data.fetchall()]
                    
                    vocabulary_item = VocabularyItem(phrase = phrase_item, translations=translation_item, notes=note_item)
                    phrases.append(vocabulary_item)

            body = Vocabulary(items = phrases)
            doc = Document(header=header, body=body)

            yield doc
