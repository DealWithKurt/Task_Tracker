from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.dependencies.auth import get_current_active_user, require_role
from app.services.comment_service import (
    get_comments as service_get_comments,
    create_comment as service_create_comment,
    delete_comment as service_delete_comment,
)

router = APIRouter()


@router.get("/tasks/{task_id}/comments", response_model=List[CommentResponse])
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return service_get_comments(db, task_id)


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(
    task_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    return service_create_comment(db, task_id, comment_in, current_user)


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    return service_delete_comment(db, comment_id, current_user)