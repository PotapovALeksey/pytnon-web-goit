from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, String
from datetime import datetime
from .base import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    students: Mapped[List["Student"]] = relationship(
        cascade="all, delete", back_populates="group"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now
    )
