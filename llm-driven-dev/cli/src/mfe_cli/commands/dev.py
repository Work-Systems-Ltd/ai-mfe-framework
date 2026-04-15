"""Development environment management."""

import subprocess

import typer
from rich.console import Console

console = Console()


def dev_command(
    app_name: str = typer.Argument("", help="Specific app to run (or empty for all)"),
    build: bool = typer.Option(False, "--build", help="Rebuild images before starting"),
) -> None:
    """Start the development environment.

    With no arguments, starts all services.
    With an app name, starts only infrastructure + shell + that app.
    """
    cmd = ["docker", "compose", "up", "-d"]

    if build:
        cmd.append("--build")

    if app_name:
        # Start infrastructure + shell + specific app
        services = [
            "postgres",
            "keycloak",
            "openfga-postgres",
            "openfga-migrate",
            "openfga",
            "shell-backend",
            "shell-frontend",
            f"{app_name}-backend",
            f"{app_name}-frontend",
        ]
        cmd.extend(services)
        console.print(f"[bold]Starting infrastructure + shell + {app_name}[/bold]")
    else:
        console.print("[bold]Starting all services[/bold]")

    result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        console.print("[green]Services started successfully[/green]")
        console.print("\nAccess points:")
        console.print("  Shell:      http://localhost:5173")
        console.print("  Shell API:  http://localhost:8000")
        console.print("  Keycloak:   http://localhost:8080")
        console.print("  OpenFGA:    http://localhost:3000")
    else:
        console.print("[red]Failed to start services[/red]")
        raise typer.Exit(1)
