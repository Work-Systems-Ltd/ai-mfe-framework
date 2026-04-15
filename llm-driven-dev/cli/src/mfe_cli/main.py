"""MFE CLI entry point."""

import typer

from mfe_cli.commands.new_app import new_app_command
from mfe_cli.commands.dev import dev_command

app = typer.Typer(
    name="mfe",
    help="MFE Framework CLI - scaffold and manage micro-frontend applications.",
)

app.command("new-app")(new_app_command)
app.command("dev")(dev_command)

if __name__ == "__main__":
    app()
