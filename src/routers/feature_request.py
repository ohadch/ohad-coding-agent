from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src import FeatureRequest
from src.app import app
from src.crud.feature_request import FeatureRequestCrud

from src.database import get_db
from src.schema import FeatureRequestUpdateSchema, FeatureRequestSearchSchema, FeatureRequestCreateSchema
from src.settings import Settings, get_settings

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
    return await crud.create(
        db=db,
        data=data,
    )


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
    crud.delete(db=db, id_=id_)