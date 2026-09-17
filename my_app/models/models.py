import uuid
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from my_app.data.my_base import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username = mapped_column(String)
    useremail = mapped_column(String)

    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    invoices = relationship("Invoices", back_populates="owner")
    clients = relationship("Client", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True, default=uuid.uuid4)

    owner: Mapped["User"] = relationship(backref="projects")

class Client(Base):
    __tablename__ = "clients"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String)
    owner_id = mapped_column(Integer, ForeignKey("users.id"))

    invoices = relationship("User", back_populates="client")
    clients = relationship("Invoices", back_populates="client")

class Invoice(Base):
    __tablename__ = "invoices"

    id = mapped_column(Integer, primary_key=True, index=True)
    amount = mapped_column(Float, nullable=False)
    description = mapped_column(String)
    status = mapped_column(String, default="unpaid")
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner_id = mapped_column(Integer, ForeignKey("users.id"))
    client_id = mapped_column(Integer, ForeignKey("clients.id"))

    invoices = relationship("User", back_populates="invoices")
    clients = relationship("Invoices", back_populates="invoices")
