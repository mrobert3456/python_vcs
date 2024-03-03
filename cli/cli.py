
from typing import Annotated, List, Optional
from pathlib import Path
from cli.commands.init import Init
from cli.commands.status import Status
from cli.commands.add import Add
from cli.commands.commit import Commit
import typer

app = typer.Typer()

def print_results(is_success, message):
    if message!=None:
        if is_success:
            print(f"Command executed successfully - {message}")
        else:
            print(f"Command execution failed - {message}")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pvc v1")
        raise typer.Exit()
    
@app.command()
def init():
    """
        Initialize version control on the current directory
    """
    init_command = Init()
    is_success, message = init_command.execute()
    print_results(is_success,message)

@app.command()
def status():
    """
        Shows the current changes
    """
    status_command = Status()
    is_success, message = status_command.execute()
    print_results(is_success,message)

@app.command()
def add(files: List[Path]):
    """
        Adds the specified files from status into staging area
    """
    add_command = Add()
    files_to_add = [str(item) for item in files]
    is_success, message = add_command.execute(files=files_to_add)
    print_results(is_success,message)

@app.command()
def commit(message):
    commit_command = Commit()
    is_success, message = commit_command.execute(message)
    print_results(is_success,message)

@app.command()
def restore(files: List[Path]):
    """
        Restore changes from the staging area
    """
    add_command = Add()
    files_to_add = [str(item) for item in files]
    is_success, message = add_command.undo(files=files_to_add)
    print_results(is_success,message)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
):
    return