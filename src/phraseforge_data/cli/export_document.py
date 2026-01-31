import os
import click

from ..lib import (
    Database,
)

from .helpers import (
    parse_selector,
)

@click.command('export')
@click.pass_context
@click.argument('selector', nargs=1, required=True)
@click.argument('output', nargs=1, type=click.Path(exists=True, writable=True, resolve_path=True, file_okay=False, dir_okay=True))
def export_document(ctx, selector, output):
    select_type, select_document, select_chunk = parse_selector(selector)
    current_filename = None
    with Database(**ctx.obj) as db:
        for doc in db.find_document(
            document_type=select_type,
            document_id = select_document,
            chunk_id = select_chunk,
            items = True):

            header = doc.header
            filename = os.path.join(output, f'{header.document}-{header.type.value}-{header.translation}.ff')
            with open(filename, "a", encoding='utf-8') as f:
                if filename != current_filename:
                    print(filename)
                    f.write(header.yaml())
                    current_filename = filename
                f.write(f'\n=== {header.chunk} ===\n\n')
                f.write(str(doc.body))
                f.write("\n")