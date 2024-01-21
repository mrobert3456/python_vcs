
from typing import Optional
from cli.commands.init import Init
from cli.commands.status import Status
import typer

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
    init_command = Init()
    if(init_command.execute()):
        print("Version control is initialized successfully")
    else:
        print("Version control is already initialized on this project")


@app.command()
def status():
    """
        Shows the current changes
    """
    status_command = Status()
    if(status_command.execute()):
        print("")
    else:
        print("Version control system is not initialized")


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