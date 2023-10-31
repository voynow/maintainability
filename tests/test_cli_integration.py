import os

import dotenv
from click.testing import CliRunner

from maintainability.cli import main

dotenv.load_dotenv()
MAINTAINABILITY_API_KEY = os.getenv("MAINTAINABILITY_API_KEY")


def test_cli_command():
    runner = CliRunner()
    args = ["--paths", "test_file.txt", "--api_key", MAINTAINABILITY_API_KEY]
    with runner.isolated_filesystem():
        with open("test_file.txt", "w") as f:
            f.write("print('hello world')\n" * 100)

        result = runner.invoke(main.cli_runner, args)
    # for debugging
    print(result.output)
    print(result.exception)
    print(result.exit_code)
    assert result.exit_code == 0
