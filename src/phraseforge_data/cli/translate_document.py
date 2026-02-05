import click

from ..lib import (
    Database,
    translate,
)

from .helpers import (
    parse_selector,
    save_document,
)

@click.command('translate')
@click.pass_context
@click.argument('selector', nargs=1, required=True)
@click.argument('output', nargs=1, type=click.Path(exists=True, writable=True, resolve_path=True, file_okay=False, dir_okay=True))
def translate_document(ctx, selector, output):
    select_type, select_document, select_chunk = parse_selector(selector)
    with Database(**ctx.obj) as db:
        for doc in db.find_document(
            document_type=select_type,
            document_id = select_document,
            chunk_id = select_chunk,
            items = True):

            doc = translate(document = doc, database = db)
            print(save_document(output, doc))