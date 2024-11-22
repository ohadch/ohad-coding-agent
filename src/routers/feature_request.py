import re
import shutil
import uuid
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src import FeatureRequest
from src.app import app
from src.crud.feature_request import FeatureRequestCrud

from src.database import get_db
from src.schema import FeatureRequestUpdateSchema, FeatureRequestSearchSchema, FeatureRequestCreateSchema
from src.services.git_service import GitService
from src.settings import Settings, get_settings
from src.types.enums import FeatureRequestState

crud = FeatureRequestCrud()
prefix = "feature_requests"
tags = [prefix]


@app.post(
    f"/{prefix}/search",
    tags=tags,
    response_model=List[FeatureRequest],
    summary=f"Search {prefix}",
)
async def search(
    page: int = 1,
    page_size: Optional[int] = None,
    filters: Optional[FeatureRequestSearchSchema] = None,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """
    Search feature_requests
    :param page: Page number
    :param page_size: Page size
    :param filters: Filters
    :param db: Database session
    :param settings: Settings
    :return: List of feature_requests
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
    response_model=FeatureRequest,
    summary=f"Create {prefix}",
)
async def create(data: FeatureRequestCreateSchema, db: Session = Depends(get_db)):
    """
    Create feature_request
    :param data: Data
    :param db: Database session
    """
    settings = get_settings()

    feature_branch_name = re.sub(r'\s+', '_', data.title.lower()) + f"_{str(uuid.uuid4())[:8]}"
    git_repo_local_path = f"{settings.git_repos_path}/{feature_branch_name}"

    feature_request = await crud.create(
        db=db,
        data=FeatureRequest(
            title=data.title,
            prompt=data.prompt,
            state=FeatureRequestState.BACKLOG,
            git_repo_remote_url=data.git_repo_remote_url,
            git_repo_local_path=git_repo_local_path,
            feature_branch=feature_branch_name,
            source_branch=data.source_branch,
        ),
    )

    git_service = GitService()

    git_service.clone_repo(
        remote_repo_url=feature_request.git_repo_remote_url,
        local_repo_path=git_repo_local_path
    )

    if feature_request.git_repo_local_path and feature_request.feature_branch:
        git_service.checkout(
            local_repo_path=feature_request.git_repo_local_path,
            source_branch=feature_request.source_branch,
            feature_branch=feature_request.feature_branch
        )

    return feature_request

@app.get(
    f"/{prefix}/{{id_}}",
    tags=tags,
    response_model=FeatureRequest,
    summary=f"Get {prefix} by ID",
)
async def get_by_id(id_: int, db: Session = Depends(get_db)):
    """
    Read feature_request by ID
    :param id_: FeatureRequest ID
    :param db: Database session
    :return: FeatureRequest
    """
    feature_request = await crud.get_by_id(db=db, id_=id_)
    if not feature_request:
        raise HTTPException(status_code=404, detail=f"{prefix.title()} not found")
    return feature_request


@app.put(
    f"/{prefix}/{{id_}}",
    tags=tags,
    response_model=FeatureRequest,
    summary=f"Update {prefix}",
)
async def update(
    id_: int,
    data: FeatureRequestUpdateSchema,
    db: Session = Depends(get_db),
):
    """
    Update feature_request
    :param id_: FeatureRequest ID
    :param data: Data to update
    :param db: Database session
    :return: Updated feature_request
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
    Delete feature_request
    :param id_: FeatureRequest ID
    :param db: Database session
    """
    # Delete the git repo
    feature_request = crud.get_by_id(db=db, id_=id_)

    if len(feature_request.git_repo_local_path) < 20:
        raise ValueError(f"Invalid git_repo_local_path: {feature_request.git_repo_local_path}")

    shutil.rmtree(feature_request.git_repo_local_path)

    crud.delete(db=db, id_=id_)