from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(routes.api_key_middleware)
app.include_router(routes.router)
