import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from my_app.data.my_base import Base

class AICheckPoint(Base):
    __tablename__ = 'ai_checkpoints'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    remote_url = Column(String, nullable=False) # conne ts to localhost:8001
    task_type = Column(String, default='classification')
    input_schema = Column(JSONB, default={})
    output_schema = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), serber_default=func.now())
