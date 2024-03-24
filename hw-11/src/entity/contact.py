from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Date, DateTime
from datetime import datetime, date
from src.entity.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str]
    phone: Mapped[str] = mapped_column(String(20))
    birthday: Mapped[date] = mapped_column(Date())

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
