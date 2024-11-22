from uuid import UUID

from ..models import FeatureRequest
from ..schema import (
    FeatureRequestSearchSchema,
    FeatureRequestCreateSchema,
    FeatureRequestUpdateSchema,
)
from ..utils.crud import GenericModelCrud


class FeatureRequestCrud(
    GenericModelCrud[
        FeatureRequest,
        UUID,
        FeatureRequest,
        FeatureRequestSearchSchema,
        FeatureRequestCreateSchema,
        FeatureRequestUpdateSchema,
    ]
):
    def __init__(self):
        super().__init__(model=FeatureRequest)