from fastapi import FastAPI, HTTPException
from typing import Dict
from maintainability.common.models import CompositeMetrics
from maintainability.common import utils

app = FastAPI()


@app.post("/submit_metrics")
async def submit_metrics(metrics: Dict[str, CompositeMetrics]):
    utils.write_metrics(metrics)
    return {"status": "ok", "message": "Metrics submitted successfully."}
