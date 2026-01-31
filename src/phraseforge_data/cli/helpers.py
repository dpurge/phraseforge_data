from pathlib import Path
from typing import Generator, Optional, Tuple
from click import (
    FileError,
    BadArgumentUsage,
    ClickException,
)

from ..lib import (
    FileFormat,
    DataType,
    Script,
    Language,
    read_phraseforge_data,
    read_yaml_data,
    read_json_data,
    read_markdown_data,
)

def get_files(input: list[str]) -> Generator[Path]:
    for i in input:
        p = Path(i)
        if not p.exists():
            raise FileError(p)
        if p.is_file():
            yield p
        if p.is_dir():
            for j in p.rglob('*'):
                if j.is_file():
                    yield j

def suffix_to_file_format(suffix: str) -> Optional[FileFormat]:
    file_format = None

    if suffix == '.ff':
        file_format = FileFormat.Phraseforge
    elif suffix == '.md':
        file_format = FileFormat.Markdown
    elif suffix == '.yaml' or suffix == '.yml':
        file_format = FileFormat.YAML
    elif suffix == '.json':
        file_format = FileFormat.JSON
    
    return file_format

def suffix_to_data_reader(suffix: str) -> callable:
    file_format = suffix_to_file_format(suffix)
    data_reader = None

    if file_format == FileFormat.Phraseforge:
        data_reader = read_phraseforge_data
    elif file_format == FileFormat.YAML:
        data_reader = read_yaml_data
    elif file_format == FileFormat.JSON:
        data_reader = read_json_data
    elif file_format == FileFormat.Markdown:
        data_reader = read_markdown_data
    # else:
    #     raise ClickException(f'Cannot read file with extension "{suffix}" as PhraseForge data')

    return data_reader

def name_to_data_type(name: str) -> Optional[DataType]:
    data_type = None

    if 'vocabulary' in name:
        data_type = DataType.Vocabulary
    elif 'model' in name:
        data_type = DataType.Model
    elif 'text' in name:
        data_type = DataType.Text
    elif 'dialog' in name:
        data_type = DataType.Dialog
    
    return data_type

def get_default_script_for_language(language: Language) -> Script:
    # Latin is the default script
    script = Script.Latin

    if language in (
        Language.Bulgarian,
        Language.Tajik,
        Language.Ukrainian,
    ):
        script = Script.Cyrillic

    if language in (
        Language.Arabic,
        Language.Persian,
        Language.Urdu,
    ):
        script = Script.Arabic

    if language in (
        Language.Chinese,
    ):
        script = Script.HanSimplified

    if language in (
        Language.Greek,
    ):
        script = Script.Greek

    return script

def parse_context(context: str) -> Tuple[str,str,str,str]:

    phrase_language = None
    translation_language = None
    phrase_script = None
    translation_script = None

    if not '/' in context:
        raise BadArgumentUsage('phrase and translation language must be separated by "/"')
    
    phrase_language, translation_language = context.split('/', maxsplit=1)

    if '-' in phrase_language:
        phrase_language, phrase_script = phrase_language.split('-', maxsplit=1)

    if not phrase_language in Language:
        raise BadArgumentUsage(f'invalid phrase language "{phrase_language}"\nAllowed languages: {', '.join(Language)}')

    if not phrase_script:
        phrase_script = get_default_script_for_language(phrase_language).value

    if not phrase_script in Script:
        raise BadArgumentUsage(f'invalid phrase script "{phrase_script}"\nAllowed scripts: {', '.join(Script)}')

    if '-' in translation_language:
        translation_language, translation_script = translation_language.split('-', maxsplit=1)

    if not translation_language in Language:
        raise BadArgumentUsage(f'invalid translation language "{translation_language}"\nAllowed languages: {', '.join(Language)}')

    if not translation_script:
        translation_script = get_default_script_for_language(translation_language).value

    if not translation_script in Script:
        raise BadArgumentUsage(f'invalid translation script "{translation_script}"\nAllowed scripts: {', '.join(Script)}')
    
    return phrase_language, phrase_script, translation_language, translation_script

def parse_selector(selector: str) -> Tuple[DataType, Optional[str], Optional[str]]:
    data_type = None
    document_id = None
    chunk_id = None

    t = selector
    if '[' in t and t.endswith(']'):
        t = t.rstrip(']')
        t, document_id = t.split('[', maxsplit=1)
        if '/' in document_id:
            document_id, chunk_id = document_id.split('/', maxsplit=1)
            if not chunk_id: chunk_id = None
        if not document_id: document_id = None

    for i in DataType:
        if i.value == t:
            data_type = i
            break

    if not data_type:
        raise BadArgumentUsage(f'Unknown data type: {t}')

    return data_type, document_id, chunk_id