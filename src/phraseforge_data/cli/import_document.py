import click

from ..lib import (
    Database,
)

from .helpers import (
    get_files,
    suffix_to_data_reader,
)

@click.command('import')
@click.pass_context
@click.argument('input', nargs=-1, type=click.Path(exists=True, readable=True, resolve_path=True))
def import_document(ctx, input):
    reader = {}
    files = get_files(input)
    with Database(**ctx.obj) as db:
        for f in files:
            suffix = f.suffix
            if not suffix in reader:
                reader[suffix] = suffix_to_data_reader(suffix)

            read_document = reader[suffix]
            if not read_document: continue

            for document in read_document(f):
                header = document.header
                if ctx.obj['data'] == header.data and ctx.obj['translation'] == header.translation:
                    doctype = header.type
                    if doctype == 'vocabulary':
                        db.import_vocabulary(document)
                    else:
                        raise click.ClickException(f'Document type cannot be imported: {doctype}')