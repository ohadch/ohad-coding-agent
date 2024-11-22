from pydantic import BaseModel


class GitRepositoryCreateSchema(BaseModel):
    local_path: str
    remote_url: str


class GitRepositoryUpdateSchema(BaseModel):
    local_path: str
    remote_url: str


class GitRepositorySearchSchema(BaseModel):
    local_path: str
    remote_url: str
