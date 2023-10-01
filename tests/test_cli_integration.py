from click.testing import CliRunner
from maintainability.cli.src import cli


def test_cli_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test_file.txt", "w") as f:
            f.write("test content")
        result = runner.invoke(cli.cli, ["--paths", "test_file.txt"])
    assert result.exit_code == 0
