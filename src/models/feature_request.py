
from src.models.base import BaseTable
from src.types.enums import FeatureRequestState


class FeatureRequest(BaseTable):

    __tablename__ = "feature_requests"

    title: str
    prompt: str
    state: FeatureRequestState
