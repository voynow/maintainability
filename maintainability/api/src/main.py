import logging
import uuid
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException

from . import config, metrics_manager, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/health")
def read_root():
    return {"status": "ok"}


@app.post("/submit_metrics")
async def submit_metrics(metrics: Dict[str, models.CompositeMetrics]):
    metrics_manager.write_metrics(metrics)
    return {"status": "ok", "message": "Metrics submitted successfully."}


@app.post("/extract_metrics")
async def extract_metrics(repo: Dict[str, str]):
    session_id = str(uuid.uuid4())
    composite_metrics: Dict[str, metrics_manager.CompositeMetrics] = {}
    try:
        print("Inside /extract_metrics endpoint")
        for filepath, code in repo.items():
            if len(code.splitlines()) > config.MIN_NUM_LINES:
                print(f"Composing metrics for {filepath}")
                composite_metrics[filepath] = metrics_manager.compose_metrics(
                    Path(filepath), code, session_id
                )
    except Exception as e:
        logger.exception("An error occurred in /extract_metrics")
        raise HTTPException(status_code=500, detail=str(e))
    return composite_metrics
