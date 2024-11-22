from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, Column
from sqlmodel import Field, SQLModel

from src.types.enums import FeatureRequestState


class FeatureRequest(SQLModel, table=True):

    __tablename__ = "feature_requests"

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
    title: str
    prompt: str
    state: FeatureRequestState
    git_repo_remote_url: str
    git_repo_local_path: str
    feature_branch: str
    source_branch: str = "main"
