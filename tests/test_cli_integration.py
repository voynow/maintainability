from click.testing import CliRunner
from maintainability.cli import main


def test_cli_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test_file.txt", "w") as f:
            f.write("test content")
        result = runner.invoke(main.cli_runner, ["--paths", "test_file.txt"])
    assert result.exit_code == 0
