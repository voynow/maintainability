from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from . import middleware, routes

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(middleware.api_key_middleware)
app.include_router(routes.router)
