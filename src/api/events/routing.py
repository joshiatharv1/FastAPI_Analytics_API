import datetime
from typing import List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select
from timescaledb.hyperfunctions import time_bucket
from user_agents import parse as parse_ua


from .models import EventBucketListSchema, EventListSchema, EventCreateSchema, EventModel, EventUpdateSchema, get_utc_now
from api.db.session import get_session
router = APIRouter()

DEFAULT_LOOKUP_PAGES=[
    "/", "/about", "/pricing", "/contact", "/blog", "/products", "/login", "/signup", "/dashboard", "/settings"
]

# --- List Events ---
# TODO: Replace stub data with a real DB query once connection is confirmed.
#   results = session.exec(select(EventModel)).all()

from user_agents import parse as parse_ua

@router.get("/", response_model=List[EventBucketListSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session)
):
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES

    query = (
        select(
            bucket.label('bucket'),
            EventModel.page.label('page'),
            EventModel.user_agent.label('ua'),
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(bucket, EventModel.user_agent, EventModel.page)
        .order_by(bucket, EventModel.page)
    )
    results = session.exec(query).fetchall()

    # Enrich each row with parsed OS info
    enriched = []
    for row in results:
        ua = parse_ua(row.ua or "")
        enriched.append({
            "bucket": row.bucket,
            "page": row.page,
            "ua": row.ua,
            "os": ua.os.family,          # e.g. "Windows", "Mac OS X", "Android"
            "os_version": ua.os.version_string,  # e.g. "10", "14.0"
            "browser": ua.browser.family,
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "count": row.count,
        })
    return enriched

# @router.get("/", response_model=List[EventBucketListSchema])
# def read_events(session: Session = Depends(get_session)):
#     # query=select(EventModel).order_by(EventModel.id.desc()).limit(10)

#     # results=session.exec(query).all()
#     # return {
#     #     "results": results,
#     #     "count": len(results),
#     # }
#     bucket=time_bucket("10 sec", EventModel.time)
#     pages=['/about', '/contact', '/pages', '/pricing']
#     # start=datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=1)
#     # finish=datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=1)
#     query = (
#         select(
#             EventModel.page.label('bucket'),
#             bucket.label('page'),
#             func.count().label('count')
#             )
#             .where(EventModel.page.in_(pages))
#             .group_by(bucket, EventModel.page)
#             .order_by(bucket, EventModel.page)
#         )
#     # results = session.exec(query).all()
#     # print(results)
#     # compiled_query=query.compile(compile_kwargs={"literal_binds": True})
#     results=session.exec(query).fetchall()
#     return results




# --- Get Event ---
# TODO: Query DB and raise 404 if not found:
#   obj = session.get(EventModel, event_id)
#   if not obj: raise HTTPException(status_code=404, detail="Event not found")
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query=select(EventModel).where(EventModel.id==event_id)
    result=session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event Not Found")
    return result


# --- Create Event ---
@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)) -> EventModel:
    obj = EventModel.model_validate(payload.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)  # Refresh to get DB-generated fields (e.g. id)
    return obj


# --- Update Event ---
# TODO: Fetch existing record, apply partial update, commit, and return.
#   obj = session.get(EventModel, event_id)
#   if not obj: raise HTTPException(status_code=404, detail="Event not found")
#   obj.sqlmodel_update(payload.model_dump(exclude_unset=True))
#   session.add(obj); session.commit(); session.refresh(obj)
# @router.put("/{event_id}", response_model=EventModel)
# def update_event(event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)):
#     query=select(EventModel).where(EventModel.id==event_id)
#     obj=session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="PUT REQUEST: Event Not Found")
#     data=payload.model_dump()
#     for k,v in data.items():
#         setattr(obj, k, v)
#     obj.updated_at=get_utc_now()
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj