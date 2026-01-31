import click

from ..lib import (
    Database,
)

from .helpers import (
    parse_selector,
)

@click.command('list')
@click.pass_context
@click.argument('selector', nargs=1, required=True)
def list_document(ctx, selector: str):
    select_type, select_document, select_chunk = parse_selector(selector)
    with Database(**ctx.obj) as db:
        for doc in db.find_document(
            document_type=select_type,
            document_id = select_document,
            chunk_id = select_chunk,
            items = False):
            
            print(doc.header)