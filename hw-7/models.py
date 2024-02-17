from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

note_tag = Table(
    "note_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    records = relationship("Records", cascade="all, delete", backref="note")
    tags = relationship(
        "Tags", secondary=note_tag, backref="notes", passive_deletes=True
    )


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
