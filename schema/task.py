from pydantic import BaseModel
from typing import Optional 
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TaskUpdateRequest(TaskCreate):
    id: int  
    title: str
    description: Optional[str] = None
    completed: bool  
