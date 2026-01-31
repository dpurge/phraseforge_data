import click

from ..lib import (
    Database,
)

@click.command('export')
@click.pass_context
@click.argument('doctype', nargs=1)
@click.argument('docid', nargs=1)
@click.argument('output', nargs=1, type=click.Path(exists=False, writable=True, resolve_path=True))
def export_document(ctx, doctype, docid, output):
    with Database(**ctx.obj) as db:
        pass