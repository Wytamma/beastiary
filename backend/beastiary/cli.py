import importlib
import uuid
from pathlib import Path
from typing import List, Optional

import typer
import uvicorn
from with_cloudflared import cloudflared

from beastiary.api import api
from beastiary.db import Database
from beastiary.watch import add_startup_files, start_watch_observer

app = typer.Typer()


def address_is_available(host: str, port: str) -> bool:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, int(port))) != 0


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    log_files: Optional[List[Path]] = typer.Argument(
        None,
        metavar="[LOG_FILE]...",
        help="Optional path to log file(s) to add at start up.",
    ),
    watch: Optional[List[Path]] = typer.Option(
        None,
        "--watch",
        help=(
            "Watch a directory or glob pattern for new log files, "
            "for example --watch logs --watch logs/*.log."
        ),
    ),
    version: bool = typer.Option(
        False, "--version", "-v", help="Display version number."
    ),
    token: str = typer.Option(str(uuid.uuid4()), "--token", "-t"),
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(5000, "--port"),
    share: bool = typer.Option(
        False, "--share", help="Create a publicly shareable link."
    ),
    no_security: bool = typer.Option(
        False, "--no-security", help="Turn off token requirement."
    ),
    delimiter: str = typer.Option(
        "\t", "--delimiter", help="Delimiter to split file columns on. Default is tab."
    ),
    debug: bool = typer.Option(False, "--debug", help="Set debug mode."),
    testing: bool = typer.Option(False, help="Only for testing.", hidden=True),
) -> None:
    """
    Realtime and remote trace inspection with BEASTIARY.
    """
    db = Database()
    db.create_table("Trace")
    db.create_table("Sample")
    setattr(api, "db", db)
    if version:
        version_info = importlib.metadata.version("beastiary")
        typer.echo(f"Beastiary {version_info}")
        return typer.Exit()
    if not address_is_available(host, port):
        typer.secho(
            f"Address {host}:{port} is already in use. Please choose another address.",
            fg=typer.colors.RED,
        )
        return typer.Exit(1)
    msg = typer.style("STARTING BEASTIARY", fg=typer.colors.BLUE, bold=True)
    typer.echo(f"\n🐙🐁 {msg} 🐁🐙\n")
    if log_files:
        add_startup_files(api.db, log_files, delimiter)
    observer = None
    if watch:
        observer = start_watch_observer(api.db, watch, delimiter)
        typer.echo("Watching for new log files:")
        for spec in watch:
            typer.echo(f"👀 - {spec}")
        typer.echo("")

    if no_security:
        warning = typer.style("WARNING", fg=typer.colors.YELLOW, bold=True)
        typer.echo(f"{warning}: Security disabled!")
        setattr(api, "security", False)
    setattr(api, "token", token)
    destination = (
        f"http://{host}:{port}/"
        if no_security
        else f"http://{host}:{port}/login?token={token}"
    )
    url = typer.style(destination, fg=typer.colors.GREEN, bold=False)
    typer.echo(f"Go to: {url}\n")
    if not no_security:
        typer.echo(f"If prompted enter token: {token}\n")
    else:
        typer.echo("Authentication is disabled.\n")
    log_level = "warning"
    if debug:
        log_level = "debug"
    if testing:
        if observer:
            observer.stop()
            observer.join()
        return typer.Exit()
    try:
        if share:
            typer.echo("Creating public shareable link...")
            with cloudflared(port=port) as cloudflared_url:
                public_destination = (
                    f"{cloudflared_url}/"
                    if no_security
                    else f"{cloudflared_url}/login?token={token}"
                )
                url_with_token = typer.style(
                    public_destination,
                    fg=typer.colors.GREEN,
                    bold=False,
                )
                typer.echo(
                    f"\nBeastiary is now publicly accessible at: {url_with_token}"
                )
                uvicorn.run(api, host=host, port=port, log_level=log_level)
        else:
            uvicorn.run(api, host=host, port=port, log_level=log_level)
    finally:
        if observer:
            observer.stop()
            observer.join()
