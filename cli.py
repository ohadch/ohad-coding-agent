from dotenv import load_dotenv
load_dotenv()

from src import get_settings


from src.services.coding_service import CodingService
from src.services.repository_reader_service import RepositoryReaderService

if __name__ == '__main__':
    while True:
        settings = get_settings()
        local_repo_path = settings.repo_path

        include_files = input("Do you want to include only specific files? "
                              "If yes, write the file names separated by commas. If no, press enter.\n"
                              "files: ")
        include_files = include_files.split(",") if include_files else None

        contents = RepositoryReaderService().read_files(directory=local_repo_path, include_files=include_files)

        print(f"Read {len(contents)} files from {local_repo_path}")
        task = input("What do you want me to do? ")

        coding_service = CodingService()
        coding_service.learn_code(file_abs_path_to_content=contents)
        code_feature_files = coding_service.code_feature(
            task=task,
            local_repo_path=local_repo_path
        )
        coding_service.write_code(
            coded_files=code_feature_files,
            local_repo_path=local_repo_path
        )

        print(f"Code written to {local_repo_path} successfully.")
        continue_execution = input("Do you want me to do something else? (yes/no) ")

        if continue_execution.lower() in ["no", "n"]:
            break
        else:
            print("Great! Let's do something else.")
            continue