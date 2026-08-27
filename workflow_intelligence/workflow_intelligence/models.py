
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text

from .database import Base


class WorkItem(Base):

    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=False)

    category = Column(String(50), nullable=False)

    priority = Column(String(20), nullable=False)

    status = Column(String(20), nullable=False)

    estimated_hours = Column(Float, nullable=False)

    dependency_count = Column(Integer, nullable=False)

    issue_count = Column(Integer, nullable=False)

    hours_since_update = Column(Float, nullable=False)

    due_date = Column(DateTime, nullable=False)

    risk_level = Column(String(20), nullable=False)

    risk_score = Column(Float, nullable=False)

    top_factors = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
