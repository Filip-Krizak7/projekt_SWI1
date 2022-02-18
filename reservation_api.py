import logging
from pathlib import Path

import typer
import uvicorn

logger = logging.getLogger()
logger.disabled = True

app = typer.Typer(help="Testing reservation service client")

@app.command()
def start(host: str = "0.0.0.0", port: int = 8800, log_level: str = "info"):
    """Run the service on port 8800, default host is 0.0.0.0"""
    uvicorn.run("main:app", host=host, port=port, log_level=log_level)

if __name__ == "__main__":
    app()