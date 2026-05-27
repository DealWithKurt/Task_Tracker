from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, CheckConstraint, Date, Index
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default='new')
    priority = Column(String(10), nullable=False, default='medium')
    deadline = Column(Date, nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    assignee = relationship("User")

    __table_args__ = (
        CheckConstraint('length(title) >= 3', name='title_length_check'),
        CheckConstraint(status.in_(['new', 'in_progress', 'done', 'cancelled']), name='status_check'),
        CheckConstraint(priority.in_(['low', 'medium', 'high']), name='priority_check'),
        Index('idx_tasks_status', 'status'),
        Index('idx_tasks_priority', 'priority'),
        Index('idx_tasks_assignee', 'assignee_id'),
        Index('idx_tasks_deadline', 'deadline')
    )
