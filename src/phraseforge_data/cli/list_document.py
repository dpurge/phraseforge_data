import click

from ..lib import (
    Database,
    DataType,
)

@click.command('list')
@click.pass_context
@click.argument('document_type', nargs=1, type=DataType)
@click.argument('selector', nargs=1, required=False)
def list_document(ctx, document_type: DataType, selector: str):

    # if not doctype in DataType:
    #     raise click.BadArgumentUsage(f'invalid document type "{doctype}"\nAllowed document types: {', '.join(DataType)}')

    select_document = None
    select_chunk = None
    if selector:
        if '/' in selector:
            select_document, select_chunk = selector.split('/', maxsplit=1)
        else:
            select_document = selector
    
    with Database(**ctx.obj) as db:
        for doc in db.find_document(
            document_type=document_type,
            document_id = select_document,
            chunk_id = select_chunk,
            items = False):

            header = doc.header
            print(f'{header.type.value}[{header.document}/{header.chunk}]\t{header.created.strftime("%Y-%m-%d %H:%M:%S")}\t{header.description}')
