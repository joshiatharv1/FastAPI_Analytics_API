from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, SQLModel
import sqlmodel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now

##Helper Method
# def get_utc_now():
#     return datetime.now(timezone.utc)


# --- DB Table Model ---
# `table=True` tells SQLModel to create an actual DB table for this model.
# Without it, it behaves as a schema/validator only (no table created).
class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)
    user_agent: Optional[str] = ""
    ip_address: Optional[str] = ""
    refferer: Optional[str] = ""        # note: typo — consider `referrer`
    session_id: Optional[str] = Field(default=None, index=True)
    duration: Optional[int] = None
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )
    # id: Optional[int] = Field(default=None, primary_key=True)
    # page: str =Field(index=True)
    # description: Optional[str] = ""
    # created_at: datetime=Field(
    #     default_factory=get_utc_now, 
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )
    # updated_at: datetime=Field(
    #     default_factory=get_utc_now, 
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )
    __chunk_time_interval__="INTERVAL 1 day"
    __drop_after__="INTERVAL 3 days"


# --- Response Schemas ---
# Used as FastAPI response types — never written directly to the DB.

class EventListSchema(SQLModel):
    """Paginated list of events."""
    results: List[EventModel]
    count: int
    
class EventBucketListSchema(SQLModel):
    """Paginated list of bucket events."""
    bucket:datetime
    page: str
    count: int

# --- Request Schemas ---
# Used to validate incoming request bodies.

class EventCreateSchema(SQLModel):
    """Payload for creating a new event. Only requires `page`."""
    page: str
    user_agent: Optional[str] = ""
    ip_address: Optional[str] = ""
    refferer: Optional[str] = ""
    session_id: Optional[str] = None
    duration: Optional[int] = None

class EventUpdateSchema(SQLModel):
    """Payload for updating an event's description."""
    description: str
    