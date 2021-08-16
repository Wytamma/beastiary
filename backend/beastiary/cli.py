from beastiary import schemas
from beastiary.api.core import add_trace
from fastapi.params import Security
import typer
import uvicorn

from .api import api
from beastiary.db.init_db import init_db
from beastiary.db.session import SessionLocal
import uuid
from pathlib import Path
from typing import List, Optional
import errno
import os

app = typer.Typer()

db = SessionLocal()
init_db(db)


@app.command()
def main(
    log_files: Optional[List[Path]] = typer.Argument(
        None,
        metavar="[LOG_FILE]...",
        help="Optional path to log file(s) to add at start up.",
    ),
    debug: bool = typer.Option(False, help="Set debug mode."),
    security: bool = typer.Option(True, help="Turn off token requirement."),
    token: str = typer.Option(str(uuid.uuid4())),
    host: str = typer.Option("127.0.0.1"),
    port: str = typer.Option(5000),
    testing: bool = typer.Option(False, help="Only for testing.", hidden=True),
):
    """
    Realtime and remote trace inspection with BEASTIARY.
    """
    msg = typer.style("STARTING BEASTIARY", fg=typer.colors.BLUE, bold=True)
    typer.echo(f"\n🐁 {msg} 🐁\n")
    if log_files:
        typer.echo(f"Adding log files:")
        for path in log_files:
            if not path.is_file():
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
            trace = add_trace(db, schemas.TraceCreate(path=str(path)))
            typer.echo(f"{trace.id} - {path} ✅")
        typer.echo("")
    url = typer.style(
        f"http://{host}:{port}/login?token={token}", fg=typer.colors.GREEN, bold=False
    )
    typer.echo(f"Go to: {url}")
    token_echo = typer.style(token, fg=typer.colors.GREEN, bold=False)
    typer.echo(f"If prompted enter token: {token}")
    api.token = token
    log_level = "warning"
    api.security = False
    if security:
        api.security = True
    if debug:
        log_level = "debug"
    if not testing:
        uvicorn.run(api, host=host, port=port, log_level=log_level)
