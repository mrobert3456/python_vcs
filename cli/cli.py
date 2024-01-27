
from typing import Annotated, List, Optional
from pathlib import Path
from cli.commands.init import Init
from cli.commands.status import Status
from cli.commands.add import Add
import typer
from cli.exceptions.pvc_already_initalized_exception import PVCAlreadyInitializedException
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pvc v1")
        raise typer.Exit()
    
@app.command()
def init():
    """
        Initialize version control on the current directory
    """
    try:
        init_command = Init()
        init_command.execute()
        print("Version control is initialized successfully")
    except PVCAlreadyInitializedException as e:
        print(e)

@app.command()
def status():
    """
        Shows the current changes
    """
    try:
        status_command = Status()
        print(status_command.execute())

    except PVCNotInitializedException as e:
        print(e)

@app.command()
def add(files: List[Path]):
    """
        Adds the specified files and directories into status and staging area
    """
    try:
        add_command = Add()
        files_to_add = [str(item) for item in files]
        print(add_command.execute(files=files_to_add))
        
    except PVCNotInitializedException as e:
        print(e)

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