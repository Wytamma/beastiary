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
    host: str = typer.Argument("127.0.0.1"),
    port: str = typer.Argument(5000),
):
    """
    Realtime and remote trace inspection with BEASTIARY.
    """
    typer.echo("🐁 STARTING BEASTIARY 🐁")
    _uuid = str(uuid.uuid4())
    typer.echo(f"Go to http://{host}:{port}/?uuid={_uuid}")
    typer.echo(f"Enter uuid: {_uuid} if prompted.")
    api.uuid = _uuid
    log_level = "warning"
    if debug:
        api.uuid = None
        log_level = "debug"
    uvicorn.run(api, host=host, port=port, log_level=log_level)
