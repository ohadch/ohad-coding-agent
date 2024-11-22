from pydantic import BaseModel

from src.types.enums import CodedFileAction


class LlmMessage(BaseModel):
    role: str
    content: str


class CodedFileResponse(BaseModel):
    file_path: str
    content: str
    action: CodedFileAction
