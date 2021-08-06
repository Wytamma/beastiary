import typer
import uvicorn

from .api import app as api
from beastiary.db.init_db import init_db
from beastiary.db.session import SessionLocal
import uuid

app = typer.Typer()

db = SessionLocal()
init_db(db)


@app.callback()
def main():
    """
    Real-time trace for BEAST
    """


@app.command()
def ui(
    debug: bool = typer.Option(False, help="Set debug mode."),
    host: str = typer.Argument("127.0.0.1"),
    port: str = typer.Argument(5000),
):
    """
    Start the application
    """
    typer.echo("🐁 STARTING BEASTIARY 🐁")
    # typer.launch("http://0.0.0.0:5000")
    if debug:
        api.uuid = None
        uvicorn.run(api, host=host, port=port, log_level="debug")
    else:
        api.uuid = str(uuid.uuid4())
        typer.echo(f"UUID: {api.uuid}")
        uvicorn.run(api, host=host, port=port, log_level="warning")
