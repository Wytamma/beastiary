import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Real-time trace for BEAST
    """


@app.command()
def test():
    """
    test command
    """
    typer.echo("TESTING")
