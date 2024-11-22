from typing import Optional

from pydantic import BaseModel

from src.types.enums import FeatureRequestState


class FeatureRequestCreateSchema(BaseModel):
    title: str
    prompt: str
    git_repo_remote_url: str = None
    source_branch: str = "main"


class FeatureRequestUpdateSchema(BaseModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    git_repo_local_path: Optional[str] = None
    git_repo_remote_url: Optional[str] = None
    source_branch: Optional[str] = None
    feature_branch: Optional[str] = None
    state: Optional[FeatureRequestState] = None


class FeatureRequestSearchSchema(BaseModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    git_repo_local_path: Optional[str] = None
    git_repo_remote_url: Optional[str] = None
    source_branch: Optional[str] = None
    feature_branch: Optional[str] = None
    state: Optional[FeatureRequestState] = None
