from uuid import UUID

from ..models import GitRepository
from ..schema import (
    GitRepositorySearchSchema,
    GitRepositoryCreateSchema,
    GitRepositoryUpdateSchema,
)
from ..utils.crud import GenericModelCrud


class GitRepositoryCrud(
    GenericModelCrud[
        GitRepository,
        UUID,
        GitRepository,
        GitRepositorySearchSchema,
        GitRepositoryCreateSchema,
        GitRepositoryUpdateSchema,
    ]
):
    def __init__(self):
        super().__init__(model=GitRepository)