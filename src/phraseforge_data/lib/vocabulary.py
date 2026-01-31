from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .basetype import (
    Language,
    Script,
    Phrase,
    Translation,
    Note,
)

class VocabularyItem(BaseModel):
    id: str
    phrase : Phrase
    translation : List[Translation] = []
    note : List[Note] = []

class VocabularyList(BaseModel):
    id: str
    description: str
    items: List[VocabularyItem] = []
    phrase_language: Language
    phrase_script: Script
    translation_language: Language
    translation_script: Script
    created: Optional[datetime] = None