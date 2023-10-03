import logging
import uuid
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException

from . import config, io_operations, metrics_manager, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/health")
def read_root():
    return {"status": "ok"}


@app.post("/submit_metrics")
async def submit_metrics(metrics: Dict[str, models.CompositeMetrics]):
    io_operations.write_metrics(metrics)
    return {"status": "ok", "message": "Metrics submitted successfully."}


def compose_repo_metrics(repo: Dict[str, str]):
    session_id = str(uuid.uuid4())
    composite_metrics: Dict[str, models.CompositeMetrics] = {}

    for filepath, code in repo.items():
        if len(code.splitlines()) < config.MIN_NUM_LINES:
            io_operations.logger(
                f"Skipping {filepath} because it has less than {config.MIN_NUM_LINES} lines of code."
            )
        else:
            if filepath.startswith("test") or Path(filepath).stem.endswith("test"):
                io_operations.logger(f"Skipping {filepath} because it is a test file.")
            else:
                io_operations.logger(f"Processing {filepath}...")
                composite_metrics[filepath] = metrics_manager.compose_metrics(
                    filepath, code, session_id
                )
    return composite_metrics


@app.post("/extract_metrics")
async def extract_metrics(repo: Dict[str, str]):
    try:
        return compose_repo_metrics(repo)
    except Exception as e:
        logger.exception("An error occurred in /extract_metrics")
        raise HTTPException(status_code=500, detail=str(e))
