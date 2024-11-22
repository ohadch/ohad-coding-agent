from pydantic import BaseModel


class FeatureRequestCreateSchema(BaseModel):
    title: str
    prompt: str


class FeatureRequestUpdateSchema(BaseModel):
    title: str
    prompt: str


class FeatureRequestSearchSchema(BaseModel):
    title: str
    prompt: str