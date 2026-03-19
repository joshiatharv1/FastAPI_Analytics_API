from typing import Generator
import timescaledb
import sqlmodel
from sqlmodel import SQLModel, Session

from .config import DATABASE_URL, DB_TIMEZONE


# --- Validation ---
# Fail fast at startup rather than getting a cryptic error on first DB call.
if not DATABASE_URL:
    raise NotImplementedError("DATABASE_URL must be set in your environment or .env file.")


# --- Engine ---
# The engine is a single shared instance — do not create one per request.
# For async support, swap to `sqlmodel.create_async_engine` and AsyncSession.
# engine = sqlmodel.create_engine(
#     DATABASE_URL,
#     echo=False,  # Set to True to log all SQL statements (useful for debugging)
# )
engine = timescaledb.create_engine(
    DATABASE_URL,
    timezone=DB_TIMEZONE
    # echo=False,  # Set to True to log all SQL statements (useful for debugging)
)

# --- Table Initialization ---
# Called once on startup via lifespan in main.py.
# SQLModel only creates tables that don't already exist — safe to call repeatedly.
def init_db() -> None:
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)
    print("Creating HyperTables....")
    timescaledb.metadata.create_all(engine)


# --- Session Dependency ---
# Use with FastAPI's Depends() to inject a session into route handlers.
# The `with` block ensures the session is closed after each request,
# even if an exception is raised.
#
# Usage:
#   def my_route(session: Session = Depends(get_session)):
#       ...
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session