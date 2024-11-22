from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src import GitRepository
from src.app import app
from src.crud.git_repository import GitRepositoryCrud

from src.database import get_db
from src.schema import GitRepositoryUpdateSchema, GitRepositorySearchSchema, GitRepositoryCreateSchema
from src.settings import Settings, get_settings

crud = GitRepositoryCrud()
prefix = "git_repositorys"
tags = [prefix]


@app.post(
    f"/{prefix}/search",
    tags=tags,
    response_model=List[GitRepository],
    summary=f"Search {prefix}",
)
async def search(
    page: int = 1,
    page_size: Optional[int] = None,
    filters: Optional[GitRepositorySearchSchema] = None,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """
    Search git_repositorys
    :param page: Page number
    :param page_size: Page size
    :param filters: Filters
    :param db: Database session
    :param settings: Settings
    :return: List of git_repositorys
    """
    items = await crud.search(
        db=db,
        filters=filters,
        page=page,
        page_size=page_size or settings.default_page_size,
        order_by="created_at",
        ascending=True,
    )
    return items


@app.post(
    f"/{prefix}",
    tags=tags,
    response_model=GitRepository,
    summary=f"Create {prefix}",
)
async def create(data: GitRepositoryCreateSchema, db: Session = Depends(get_db)):
    """
    Create git_repository
    :param data: Data
    :param db: Database session
    """
    return await crud.create(
        db=db,
        data=data,
    )


@app.get(
    f"/{prefix}/{{id_}}",
    tags=tags,
    response_model=GitRepository,
    summary=f"Get {prefix} by ID",
)
async def get_by_id(id_: int, db: Session = Depends(get_db)):
    """
    Read git_repository by ID
    :param id_: GitRepository ID
    :param db: Database session
    :return: GitRepository
    """
    git_repository = await crud.get_by_id(db=db, id_=id_)
    if not git_repository:
        raise HTTPException(status_code=404, detail=f"{prefix.title()} not found")
    return git_repository


@app.put(
    f"/{prefix}/{{id_}}",
    tags=tags,
    response_model=GitRepository,
    summary=f"Update {prefix}",
)
async def update(
    id_: int,
    data: GitRepositoryUpdateSchema,
    db: Session = Depends(get_db),
):
    """
    Update git_repository
    :param id_: GitRepository ID
    :param data: Data to update
    :param db: Database session
    :return: Updated git_repository
    """
    return crud.update(
        db=db,
        id_=id_,
        data=data,
    )


@app.delete(
    f"/{prefix}/{{id_}}",
    tags=tags,
    summary=f"Delete {prefix}",
)
async def delete(id_: int, db: Session = Depends(get_db)):
    """
    Delete git_repository
    :param id_: GitRepository ID
    :param db: Database session
    """
    crud.delete(db=db, id_=id_)