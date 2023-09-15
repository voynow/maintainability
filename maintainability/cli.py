from pathlib import Path

import click

from . import app


options = {
    "multiple": True,
    "type": click.Path(exists=True),
    "help": "List of paths to analyze",
    "default": ["."],
}


@click.command()
@click.option("--paths", **options)
def cli(paths):
    """Run the maintainability analysis"""
    app.main([Path(path) for path in paths])
