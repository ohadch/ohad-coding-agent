from src.models.base import BaseTable
from src.types.enums import FeatureRequestState


class FeatureRequest(BaseTable, table=True):

    __tablename__ = "feature_requests"

    title: str
    prompt: str
    state: FeatureRequestState