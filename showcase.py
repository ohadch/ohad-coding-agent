from dotenv import load_dotenv
load_dotenv()

from src import get_settings


from src.services.coding_service import CodingService
from src.services.repository_reader_service import RepositoryReaderService

if __name__ == '__main__':
    settings = get_settings()
    local_repo_path = settings.showcase_repo_path
    contents = RepositoryReaderService().read_files(directory=local_repo_path)
    coding_service = CodingService()
    coding_service.learn_code(file_abs_path_to_content=contents)
    code_feature_files = coding_service.code_feature(
        task="""
        Implement the remove_todo method in the TodoService class that is located in src/services/todo_service.py
        """,
        local_repo_path=local_repo_path
    )
    coding_service.write_code(
        coded_files=code_feature_files,
        local_repo_path=local_repo_path
    )
