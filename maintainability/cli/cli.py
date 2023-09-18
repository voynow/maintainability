from pathlib import Path

import click

from . import main

options = {
    "multiple": True,
    "type": click.Path(exists=True),
    "help": "List of paths to analyze",
    "default": ["."],
}


@click.command()
@click.option("--paths", **options)
def cli(paths):
    main.main([Path(path) for path in paths])


if __name__ == "__main__":
    cli()
