from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, func
from sqlmodel import Field, SQLModel


class GitRepository(SQLModel, table=True):

    __tablename__ = "git_repositories"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), nullable=True
        )
    )
    local_path: Optional[str] = Field(sa_column=Column(String, nullable=True, unique=True))
    remote_url: Optional[str] = Field(sa_column=Column(String, nullable=True, unique=True))
