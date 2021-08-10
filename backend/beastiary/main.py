from fastapi.params import Security
import typer
import uvicorn

from .api import app as api
from beastiary.db.init_db import init_db
from beastiary.db.session import SessionLocal
import uuid

app = typer.Typer()

db = SessionLocal()
init_db(db)


@app.command()
def main(
    debug: bool = typer.Option(False, help="Set debug mode."),
    security: bool = typer.Option(True, help="Turn off token requirement."),
    host: str = typer.Argument("127.0.0.1"),
    port: str = typer.Argument(5000),
):
    """
    Realtime and remote trace inspection with BEASTIARY.
    """
    typer.echo("🐁 STARTING BEASTIARY 🐁")
    token = str(uuid.uuid4())
    typer.echo(f"Go to http://{host}:{port}/login?token={token}")
    typer.echo(f"If prompted enter token: {token}")
    api.token = token
    log_level = "warning"
    api.security = False
    if security:
        api.security = True
    if debug:
        log_level = "debug"
    uvicorn.run(api, host=host, port=port, log_level=log_level)
