import click
from . import app


@click.command()
def cli():
    """Run the maintainability analysis"""
    app.main()
