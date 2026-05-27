from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse

class CommentBase(BaseModel):
    text: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    task_id: int
    user_id: Optional[int] = None
    created_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True
