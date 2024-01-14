from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Assistant(Base):
    __tablename__ = 'assistants'
    id = Column(String, primary_key=True)
    object_type = Column(String)
    created_at = Column(DateTime)
    name = Column(String)
    description = Column(String)
    model = Column(String)
    instructions = Column(String)
    tools = Column(JSON)
    file_ids = Column(JSON)
    assistant_metadata = Column(JSON)


class Threads(Base):
    __tablename__ = 'threads'
    id = Column(String, primary_key=True)
    object_type = Column(String)
    created_at = Column(DateTime)
    thread_metadata = Column(JSON)


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    object = Column(String)
    created_at = Column(DateTime)
    thread_id = Column(String)
    role = Column(String)
    content = Column(JSON)
    file_ids = Column(JSON)
    assistant_id = Column(String)
    run_id = Column(String)
    message_metadata = Column(JSON)
