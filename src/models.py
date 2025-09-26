from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    stargazers_count: Mapped[int] = mapped_column(Integer, default=0)
    watchers_count: Mapped[int] = mapped_column(Integer, default=0)
    forks_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    html_url: Mapped[str] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)

    # Tracking fields
    fetched_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)