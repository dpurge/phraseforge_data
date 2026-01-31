from pathlib import Path

from click import (
    BadParameter,
    ClickException,
)

from ..lib import (
    Script,
    Language,
    DataType,
    FileFormat,
)

from .helpers import (
    suffix_to_file_format,
    name_to_data_type,
    get_default_script_for_language,
)


def validate_language(ctx, param, value):
    if not value in Language:
        raise BadParameter(value)
    
    script_key = None
    if param.name == 'phrase_language':
        script_key = 'phrase_script'
    elif param.name == 'translation_language':
        script_key = 'translation_script'
    
    if script_key and not script_key in ctx.params:
        script = get_default_script_for_language(value)
        ctx.params[script_key] = script.value
        # if value in (
        #     Language.English,
        #     Language.Polish,
        # ):
        #     ctx.params[script_key] = Script.Latin.value
    
    return value

def validate_script(ctx, param, value):
    if not value and ctx.params[param.name]:
        value = ctx.params[param.name]
        
    if not value in Script:
        raise BadParameter(value)
    
    return value

def validate_data_type(ctx, param, value):
    if not value and ctx.params[param.name]:
        value = ctx.params[param.name]

    if not value in DataType:
        raise BadParameter(value)
    
    return value

def validate_file_format(ctx, param, value):
    if not value and ctx.params[param.name]:
        value = ctx.params[param.name]

    if not value in FileFormat:
        raise BadParameter(value)
    
    return value


def validate_output(ctx, param, value):
    p = Path(value)

    if p.exists():
        raise ClickException('Output already exists')
    
    if not 'file_format' in ctx.params:
        file_format = suffix_to_file_format(p.suffix)
        if file_format:
            ctx.params['file_format'] = file_format.value

    if not 'data_type' in ctx.params:
        data_type = name_to_data_type(p.stem)
        if data_type:
            ctx.params['data_type'] = data_type.value

    return p.absolute()