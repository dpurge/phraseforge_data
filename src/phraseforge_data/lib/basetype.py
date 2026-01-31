from datetime import datetime
from typing import Optional, Dict
from enum import Enum
from pydantic import BaseModel

class DataType(str, Enum):
    Vocabulary = 'vocabulary'
    Model = 'model'
    Text = 'text'
    Dialog = 'dialog'

class FileFormat(str, Enum):
    Phraseforge = 'phraseforge'
    Markdown = 'markdown'
    YAML = 'yaml'
    JSON = 'json'

class Script(str, Enum):
    Arabic = 'arab'
    # Arabic_Nastaliq = 'aran'
    Armenian = 'armn'
    # Bopomofo = 'bopo'
    Coptic = 'copt'
    Cuneiform = 'xsux'
    Cyrillic = 'cyrl'
    CyrillicChurchSlavonic = 'cyrs'
    Devanagari = 'deva'
    EgyptianHieroglyphs = 'egyp'
    Georgian = 'geor'
    Greek = 'grek'
    Gujarati = 'gujr'
    Han = 'hani'
    HanSimplified = 'hans'
    HanTraditional = 'hant'
    Hebrew = 'hebr'
    # Hiragana = 'hira'
    Japanese = 'jpan'
    Javanese = 'java'
    Jurchen = 'jurc'
    # Katakana = 'kana'
    Korean = 'kore'
    Latin = 'latn'
    # Rongorongo = 'roro'
    # Runic = 'runr'
    Syriac = 'syrc'
    Thai = 'thai'
    Tibetan = 'tibt'

class Language(str, Enum):
    Ancient_Greek = 'grc'
    Akkadian = 'akk'
    Albanian = 'sqi'
    Arabic = 'ara'
    Armenian = 'hye'
    Azerbaijani = 'aze'
    Basque = 'eus'
    Bulgarian = 'bul'
    Burmese = 'mya'
    Chinese = 'zho'
    Czech = 'ces'
    Dutch = 'nld'
    Egyptian = 'egy'
    Esperanto = 'epo'
    Estonian = 'est'
    English = 'eng'
    Persian = 'fas'
    Faroese = 'fao'
    Finnish = 'fin'
    French = 'fra'
    Gaelic = 'gla'
    Georgian = 'kat'
    German = 'deu'
    Greek = 'ell'
    Hebrew = 'heb'
    Hindi = 'hin'
    Hungarian = 'hun'
    Malay = 'msa'
    Icelandic = 'isl'
    Indonesian = 'ind'
    Irish = 'gle'
    Italian = 'ita'
    Japanese = 'jpn'
    Javanese = 'jav'
    Kazakh = 'kaz'
    Kirghiz = 'kir'
    Korean = 'kor'
    Kurdish = 'kur'
    Lao = 'lao'
    Latin = 'lat'
    Latvian = 'lav'
    Lithuanian = 'lit'
    Manchu = 'mnc'
    Mongolian = 'mon'
    Norwegian = 'nor'
    Ottoman = 'ota'
    Polish = 'pol'
    Portuguese = 'por'
    Pushto = 'pus'
    Romanian = 'ron'
    Romany = 'rom'
    Serbian = 'srp'
    Spanish = 'spa'
    Swedish = 'swe'
    Tajik = 'tgk'
    Tagalog = 'tgl'
    Thai = 'tha'
    Tibetan = 'bod'
    Turkish = 'tur'
    Turkmen = 'tuk'
    Uighur = 'uig'
    Urdu = 'urd'
    Ukrainian = 'ukr'
    Uzbek = 'uzb'
    Vietnamese = 'vie'
    Welsh = 'cym'
    Xhosa = 'xho'
    Yiddish = 'yid'
    Yoruba = 'yor'
    Zulu = 'zul'

class Grammar(BaseModel):
    text: Optional[str] = None

class Phrase(BaseModel):
    text: str
    grammar: Optional[Grammar] = None
    transcription: Optional[str] = None
    created: Optional[datetime] = datetime.now()

    def __str__(self) -> str:
        text = self.text
        # if self.grammar:
        #     text += f' {{{', '.join(self.grammar)}}}'
        if self.transcription:
            text += f' [{self.transcription}]'
        return text

class Model(BaseModel):
    phrase: Phrase
    translation: Optional[str] = None
    notes: Optional[list[str]] = None
    created: Optional[datetime] = datetime.now()

class Text(BaseModel):
    text: str
    translation: Optional[str] = None
    created: Optional[datetime] = datetime.now()

class Dialog(BaseModel):
    text: str
    translation: Optional[str] = None
    created: Optional[datetime] = datetime.now()

class VocabularyItem(BaseModel):
    # id: str
    phrase: Phrase
    translations: Optional[list[str]] = None
    notes: Optional[list[str]] = None
    created: Optional[datetime] = datetime.now()

    def __str__(self) -> str:
        text = str(self.phrase)
        if self.translations:
            text += f' = {'; '.join(self.translations)}'
        if self.notes:
            text += f'({'; '.join(self.notes)})'
        return text

class Vocabulary(BaseModel):
    # id: str
    items: list[VocabularyItem] = []

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.items])

class Language_and_Script(BaseModel):
    language: Language
    script: Script

    def __str__(self) -> str:
        return f'{self.language.value}-{self.script.value}'

class Header(BaseModel):
    document: str
    chunk: Optional[str] = None
    type: DataType
    description: Optional[str]
    data: Language_and_Script
    translation: Language_and_Script
    created: Optional[datetime] = datetime.now()

    def __str__(self) -> str:
        id = f'{self.document}/{self.chunk if self.chunk else '-'}'
        selector = f'{self.type.value}[{id}]'
        langpair = f'{self.data}/{self.translation}'
        description = self.description if self.description else '-'
        return f'{selector}\t{self.created.strftime("%Y-%m-%d %H:%M:%S")}\t{description}\t{langpair}'
    
    def yaml(self) -> str:
        indent = '  '
        lines = []
        lines.append(f'document: {self.document}')
        lines.append(f'type: {self.type.value}')
        lines.append(f'description: {self.description}')
        lines.append('data:')
        lines.append(f'{indent}language: {self.data.language.value}')
        lines.append(f'{indent}script: {self.data.script.value}')
        lines.append('translation:')
        lines.append(f'{indent}language: {self.translation.language.value}')
        lines.append(f'{indent}script: {self.translation.script.value}')
        lines.append('')
        return "\n".join(lines)

class Document(BaseModel):
    header: Header
    body: Vocabulary | Model | Text | Dialog