
from typing import Optional
from init import Init
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
    print(init_command.execute())

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