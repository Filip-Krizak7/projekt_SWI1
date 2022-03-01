import logging
from pathlib import Path

import typer
import uvicorn

logger = logging.getLogger()
logger.disabled = True

app = typer.Typer(help="Testing reservation service client")


if __name__ == "__main__":
    app()