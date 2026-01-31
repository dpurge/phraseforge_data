import re

from pathlib import Path
from typing import Generator

from .basetype import (
    DataType,
    Language,
    Script,
    Text,
    Document,
)

from .parser import (
    get_parser,
    parse_header,
)

def read_chunks(filename: str | Path) -> Generator[(str, str)]:
    id = None
    chunk = ""
    with open(filename, 'r', encoding='utf-8') as f:
        while line := f.readline():
            l = line.strip()
            if l.startswith('===') and l.endswith('==='):
                yield id, chunk.strip()
                id = l.strip('===').strip()
                chunk = ""
            else:
                chunk += line
        yield id, chunk.strip()

def read_phraseforge_data(filename: str | Path) -> Generator[Document]:
    chunks = read_chunks(filename)
    
    _, chunk = next(chunks)
    header = parse_header(chunk)

    parse = get_parser(header.type)

    for id, chunk in chunks:
        header.chunk = id
        yield Document(header=header, body=parse(chunk))

def read_yaml_data(filename: str) -> Document:
    pass

def read_json_data(filename: str) -> Document:
    pass

def read_markdown_data(filename: str) -> Document:
    pass