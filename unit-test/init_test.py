import pytest
from pathlib import Path
from cli.commands.init import Init

def test_init_creates_directories():
    init_command = Init()
    init_command.execute()

    directory_path = Path("./.pv")

    assert directory_path.is_dir(), f"Directory '{directory_path}' does not exist"
