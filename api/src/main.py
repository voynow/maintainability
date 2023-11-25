import os
import traceback
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import logger, middleware, routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.environ.get("SKIP_AUTH_MIDDLEWARE") != "True":
    app.middleware("http")(middleware.mixed_auth_middleware)

app.include_router(routers.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_data = {
        "path": request.url.path,
        "method": request.method,
        "error": f"{type(exc)}: {str(exc)}",
        "traceback": traceback.format_exc(),
    }
    logger.logger(json.dumps(log_data))
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.logger(f"HTTPException {exc.status_code}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
