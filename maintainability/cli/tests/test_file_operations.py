from unittest.mock import mock_open, patch
from pathlib import Path
from cli.src import file_operations

# Replace these with your actual configurations
MOCK_EXTENSIONS = [".py", ".js"]
MOCK_GITIGNORE = "*.log\n*.tmp"


def test_read_text():
    with patch("builtins.open", mock_open(read_data="file_content")):
        result = file_operations.read_text(Path("some_file.txt"))
    assert result == "file_content"


def test_get_ignored_patterns():
    with patch("builtins.open", mock_open(read_data=MOCK_GITIGNORE)):
        patterns = file_operations.get_ignored_patterns(Path(".gitignore"))
    assert "*.log" in patterns.patterns  # Adapt according to your mock data


@patch("pathlib.Path.iterdir")
def test_load_files(mock_iterdir):
    mock_iterdir.return_value = [Path("file1.py"), Path("file2.js"), Path("file3.log")]
    with patch("builtins.open", mock_open(read_data="file_content")):
        result = file_operations.load_files(Path("."))
    assert Path("file1.py") in result  # Adapt according to your expected results


def test_filter_repo_by_paths():
    mock_repo = {
        Path("dir1/file1.py"): "content1",
        Path("dir2/file2.py"): "content2",
    }
    with patch("file_operations.load_files", return_value=mock_repo):
        result = file_operations.filter_repo_by_paths([Path("dir1")])
    assert Path("dir1/file1.py").as_posix() in result
