import click

from ..lib import (
    Database,
    DataType,
)

from .helpers import (
    get_files,
    suffix_to_data_reader,
    parse_selector,
)

@click.command('import')
@click.pass_context
@click.argument('selector', nargs=1, required=True)
@click.argument('input', nargs=-1, type=click.Path(exists=True, readable=True, resolve_path=True))
def import_document(ctx, selector, input):
    select_type, select_document, select_chunk = parse_selector(selector)

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

                if header.type != select_type: continue
                if select_document and not header.document.startswith(select_document): continue
                if select_chunk and not header.chunk.startswith(select_chunk): continue

                if ctx.obj['data'] == header.data and ctx.obj['translation'] == header.translation:
                    if header.type == DataType.Vocabulary:
                        db.import_vocabulary(document)
                    else:
                        raise click.ClickException(f'Document type cannot be imported: {header.type}')