import yaml
from typing import Optional

from .basetype import (
    DataType,
    Header,
    Phrase,
    Vocabulary,
    VocabularyItem,
    Text,
)

from click import (
    ClickException,
)

from hashlib import md5
from base64 import urlsafe_b64encode

def get_id(*args: list[Optional[str]]) -> str:
    text = ''.join([x if x else '' for x in args]).casefold()
    if not text:
        return '-'
    md5bytes = md5(text.encode(encoding="utf-8")).digest()
    return urlsafe_b64encode(md5bytes).decode('ascii').rstrip('=')

def parse_header(text: str) -> Header:
    data = yaml.safe_load(text)
    header = Header(**data)
    return header

def parse_vocabulary(text: str) -> Vocabulary:
    items = []
    for line in text.splitlines():
        _phrase = line
        _grammar = None
        _transcription = None
        _translations = None
        _notes = None

        i = _phrase.find('=')
        if i > -1:
            _translations = _phrase[i+1:].strip()
            _phrase = _phrase[0:i].strip()

        if _phrase.endswith(']'):
            j = _phrase.find('[')
            if j > -1:
                _transcription = _phrase[j+1:-1].strip()
                _phrase = _phrase[0:j].strip()

        if _phrase.endswith('}'):
            k = _phrase.find('{')
            if k > -1:
                # _grammar = _phrase[k+1:-1].strip()
                _phrase = _phrase[0:k].strip()

        if _translations.endswith(')'):
            l = _translations.find('(')
            _notes = _translations[l+1:-1].strip()
            _translations = _translations[0:l].strip()

        phrase = Phrase(
            id = get_id(_phrase, _grammar, _transcription),
            text = _phrase,
            grammar = _grammar,
            transcription = _transcription)
        
        translations = [i.strip() for i in _translations.split(';')]
        notes = [i.strip() for i in _notes.split(';')] if _notes else None
        
        item = VocabularyItem(
            phrase = phrase,
            translations=translations,
            notes = notes)

        items.append(item)

    return Vocabulary(items=items)

def parse_text(text: str) -> Text:
    return Text(
        text=text,
        translation = None)

def get_parser(data_type: DataType) -> callable:
    if data_type == DataType.Vocabulary:
        return parse_vocabulary
    elif data_type == DataType.Text:
        return parse_text
    else:
        raise ClickException(f'No parser for {data_type.value}')