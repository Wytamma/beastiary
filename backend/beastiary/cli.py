import pkg_resources
import uuid
import typer
import uvicorn
from with_cloudflared import cloudflared

from pathlib import Path
from typing import List, Optional

from beastiary.api.core import add_trace, check_for_new_samples
from beastiary.api import api
from beastiary.db import Database
from beastiary import schemas

app = typer.Typer()


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
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
            except ValueError as e:
                typer.echo(f"❌ - {path}: {e}")
        typer.echo("")

    setattr(api, "token", token)
    url = typer.style(
        f"http://{host}:{port}/login?token={token}", fg=typer.colors.GREEN, bold=False
    )
    typer.echo(f"Go to: {url}\n")
    if no_security:
        warning = typer.style("WARNING", fg=typer.colors.YELLOW, bold=True)
        typer.echo(f"{warning}: Security disabled!")
        setattr(api, "security", False)
    else:
        typer.echo(f"If prompted enter token: {token}\n")
    log_level = "warning"
    if debug:
        log_level = "debug"
    if testing:
        typer.Exit()
    if share:
        typer.echo("Creating public shareable link...")
        with cloudflared(port=port) as cloudflared_url:
            url_with_token = typer.style(
                f"{cloudflared_url}", fg=typer.colors.GREEN, bold=False
            )
            typer.echo(f"\nBeastiary is now publicly accessible at: {url_with_token}")
            uvicorn.run(api, host=host, port=port, log_level=log_level)
    else:
        uvicorn.run(api, host=host, port=port, log_level=log_level)
