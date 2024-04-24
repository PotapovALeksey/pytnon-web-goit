from datetime import datetime

from sqlalchemy import UUID, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import uuid


from .base import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email = mapped_column(String(150), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    refresh_token = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
