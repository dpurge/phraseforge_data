from ollama import chat

from .basetype import (
    DataType,
    Document,
    Vocabulary,
    # Model,
    # Text,
    # Dialog,
    Language_and_Script,
    # Language,
    # Script,
)

from .prompt import (
    TRANSLATE_MODEL,
    TRANSLATE_SYSTEM,
    TRANSLATE_EXAMPLE,
)

from ..lib import (
    Database,
)

def get_prompt(SYSTEM: str, EXAMPLE:str, pattern: str, examples: list[dict]) -> str:
    prompt = SYSTEM.format(pattern=pattern)
    for example in examples:
        prompt += "\n" + EXAMPLE.format(**example)
    return prompt

def translate_vocabulary(source: Language_and_Script, target: Language_and_Script, vocabulary: Vocabulary, database: Database) -> Vocabulary:

    pattern = '「Translate from [SOURCE_LANGUAGE] to [TARGET_LANGUAGE]: [TEXT]」'

    for item in vocabulary.items:
        if not item.translations:
            phrase = item.phrase
            examples = []

            for i in database.find_all_vocabulary_translations(phrase = phrase):
                l, t, _ = i
                examples.append({"user": f'Translate from {source.language.name} to {l.language.name}: {phrase.text}', "assistant": f'{"; ".join(t)}'})
            
            prompt = get_prompt(SYSTEM=TRANSLATE_SYSTEM, EXAMPLE=TRANSLATE_EXAMPLE, pattern=pattern, examples=examples)
            
            response = chat(TRANSLATE_MODEL, 
                messages=[
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': f'Translate from {source.language.name} to {target.language.name}: {phrase.text}'}
                ])
            item.translations = [i.strip() for i in response.message.content.split(';')]

    return vocabulary

def translate(document: Document, database: Database) -> Document:
    if document.header.type == DataType.Vocabulary:
        document.body = translate_vocabulary(
            source = document.header.data,
            target = document.header.translation,
            vocabulary= document.body,
            database = database)
    return document

def transcribe(document: Document) -> Document:
    return document