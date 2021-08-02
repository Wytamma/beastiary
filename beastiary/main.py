import typer
import uvicorn

from .api import app as api
from beastiary.db.init_db import init_db
from beastiary.db.session import SessionLocal

app = typer.Typer()

db = SessionLocal()
init_db(db)


@app.callback()
def main():
    """
    Real-time trace for BEAST
    """


@app.command()
def ui(host: str = typer.Argument("127.0.0.1"), port: str = typer.Argument(5000)):
    """
    Start the application
    """
    typer.echo("🐁 STARTING BEASTIARY 🐁")
    typer.launch("http://0.0.0.0:5000")
    uvicorn.run(api, host=host, port=port, log_level="warning")
