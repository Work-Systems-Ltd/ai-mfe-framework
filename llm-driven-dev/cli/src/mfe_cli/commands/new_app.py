"""Scaffold a new MFE application."""

import os
from pathlib import Path

import typer
from jinja2 import Environment, FileSystemLoader
from rich.console import Console

console = Console()

SCAFFOLDS_DIR = Path(__file__).parent.parent / "scaffolds"


def new_app_command(
    name: str = typer.Argument(..., help="App name (e.g., 'inventory')"),
    display_name: str = typer.Option("", help="Display name (defaults to titlecased name)"),
    port: int = typer.Option(5175, help="Frontend dev server port"),
) -> None:
    """Scaffold a new MFE application with backend and frontend."""
    if not display_name:
        display_name = name.replace("-", " ").title()

    snake_name = name.replace("-", "_")
    app_dir = Path("apps") / name

    if app_dir.exists():
        console.print(f"[red]Error: {app_dir} already exists[/red]")
        raise typer.Exit(1)

    console.print(f"[bold]Scaffolding new MFE app: {name}[/bold]")

    env = Environment(loader=FileSystemLoader(str(SCAFFOLDS_DIR)))

    context = {
        "app_name": name,
        "app_name_snake": snake_name,
        "app_display_name": display_name,
        "app_path_prefix": f"/apps/{name}",
        "frontend_port": port,
    }

    # Create directory structure
    dirs = [
        f"backend/src/{snake_name}_app/routers",
        "backend/tests",
        "frontend/src/router",
        "frontend/src/views",
        "frontend/public",
    ]
    for d in dirs:
        (app_dir / d).mkdir(parents=True, exist_ok=True)

    # Render templates
    for template_name in env.list_templates():
        template = env.get_template(template_name)
        rendered = template.render(**context)

        # Map template paths to output paths
        output_path = app_dir / template_name.replace("__app_name__", snake_name)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered)

    console.print(f"[green]Created {app_dir}[/green]")
    console.print(f"\nNext steps:")
    console.print(f"  1. Add services to docker-compose.yml")
    console.print(f"  2. cd {app_dir}/backend && poetry install")
    console.print(f"  3. cd {app_dir}/frontend && npm install")
    console.print(f"  4. docker compose up -d --build")
