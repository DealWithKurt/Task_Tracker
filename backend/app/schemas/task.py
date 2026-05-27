from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date, datetime
from app.schemas.user import UserResponse

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="new", pattern="^(new|in_progress|done|cancelled)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    deadline: date
    assignee_id: Optional[int] = None

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_future(cls, v: date):
        if v < date.today():
            raise ValueError("Deadline cannot be earlier than current date")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(new|in_progress|done|cancelled)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    deadline: Optional[date] = None
    assignee_id: Optional[int] = None

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_future(cls, v: Optional[date]):
        if v and v < date.today():
            raise ValueError("Deadline cannot be earlier than current date")
        return v

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    assignee: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    limit: int
    pages: int
