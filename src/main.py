from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI

from api.db.session import init_db
from api.events import router as event_router


# --- Lifespan ---
# Replaces the deprecated @app.on_event("startup") / "shutdown" pattern.
# Code before `yield` runs on startup, code after runs on shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Create tables if they don't exist yet
    yield
    # Add any cleanup logic here (e.g. close connections, flush caches)


# --- App Instance ---
app = FastAPI(lifespan=lifespan)


# --- Routers ---
# Each router encapsulates a related group of endpoints.
# Prefix scopes all event routes under /api/event
app.include_router(event_router, prefix="/api/event")


# --- Core Routes ---

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
def read_api_health():
    """Health check endpoint — useful for Docker/k8s liveness probes."""
    return {"status": "ok"}