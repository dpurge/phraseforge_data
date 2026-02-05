import click

# from .validate import (
#     validate_language,
#     validate_script,
# )

from .import_document import import_document
from .export_document import export_document
from .list_document import list_document
from .translate_document import translate_document

from .helpers import (
    parse_context,
    # get_default_script_for_language,
)

from ..lib import (
    Language,
    Script,
    Language_and_Script,
)

@click.group()
@click.pass_context
@click.argument('context', nargs=1)
def cli(ctx,
    context,
) -> None:
    ctx.ensure_object(dict)

    phrase_language, phrase_script, translation_language, translation_script = parse_context(context)

    ctx.obj['data'] = Language_and_Script(
        language = phrase_language,
        script = phrase_script
    )
    
    ctx.obj['translation'] = Language_and_Script(
        language = translation_language,
        script = translation_script
    )

cli.add_command(import_document)
cli.add_command(export_document)
cli.add_command(list_document)
cli.add_command(translate_document)
