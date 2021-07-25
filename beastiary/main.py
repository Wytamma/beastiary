import typer
import uvicorn
import subprocess

from .app import app as api

app = typer.Typer()


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
    uvicorn.run(api, host=host, port=port)
