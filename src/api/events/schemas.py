from pydantic import BaseModel
from typing import List, Optional

"""
id
path
description

"""
class EventSchema(BaseModel):
    id: int
    page: Optional[str]="Default Value"
class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int

class EventCreateSchema(BaseModel):
    page:str
    

class EventUpdateSchema(BaseModel):
    description:str