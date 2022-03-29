import errno
import os
import pkg_resources
import uuid
import typer
import uvicorn

from pathlib import Path
from typing import List, Optional

from beastiary.api.core import add_trace, check_for_new_samples
from beastiary.api import api
from beastiary.db import Database
from beastiary import schemas

app = typer.Typer()


@app.command()
def main(
    log_files: Optional[List[Path]] = typer.Argument(
        None,
        metavar="[LOG_FILE]...",
        help="Optional path to log file(s) to add at start up.",
    ),
    version: bool = typer.Option(
        False, "--version", "-v", help="Display version number."
    ),
    token: str = typer.Option(str(uuid.uuid4()), "--token", "-t"),
    host: str = typer.Option("127.0.0.1", "--host"),
    port: str = typer.Option(5000, "--port"),
    security: bool = typer.Option(True, help="Turn off token requirement."),
    debug: bool = typer.Option(False, help="Set debug mode."),
    testing: bool = typer.Option(False, help="Only for testing.", hidden=True),
    delimiter: str = typer.Option(None, "--delimiter"),
) -> None:
    """
    Realtime and remote trace inspection with BEASTIARY.
    """
    db = Database()
    db.create_table("Trace")
    db.create_table("Sample")
    setattr(api, "db", db)
    if version:
        typer.echo(f"Beastiary {pkg_resources.get_distribution('beastiary').version}")
        return typer.Exit()
    msg = typer.style("STARTING BEASTIARY", fg=typer.colors.BLUE, bold=True)
    typer.echo(f"\n🐙🐁 {msg} 🐁🐙\n")
    if log_files:
        typer.echo(f"Adding log files:")
        for path in log_files:
            try:
                trace = add_trace(
                    api.db, schemas.TraceCreate(path=str(path), delimiter=delimiter)
                )
                check_for_new_samples(api.db, trace=trace)
                typer.echo(f"✅ - {trace['path']}")
            except ValueError:
                typer.echo(f"❌ - {path}")
        typer.echo("")
    url = typer.style(
        f"http://{host}:{port}/login?token={token}", fg=typer.colors.GREEN, bold=False
    )
    typer.echo(f"Go to: {url}\n")
    typer.echo(f"If prompted enter token: {token}")
    setattr(api, "token", token)
    if not security:
        warning = typer.style("WARNING", fg=typer.colors.YELLOW, bold=True)
        typer.echo(f"{warning}: Security disabled!")
        setattr(api, "security", False)
    log_level = "warning"
    if debug:
        log_level = "debug"
    if not testing:
        uvicorn.run(api, host=host, port=port, log_level=log_level)
