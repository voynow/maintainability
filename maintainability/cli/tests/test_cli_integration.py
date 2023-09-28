import requests_mock
from cli.src import cli
from click.testing import CliRunner


def test_cli_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["--paths", ""])
    assert result.exit_code == 0
    assert "expected_output" in result.output
