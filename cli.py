from dotenv import load_dotenv
load_dotenv()

from typing import Dict, List

from pydantic import BaseModel

from src import get_settings


from src.services.coding_service import CodingService
from src.services.repository_reader_service import RepositoryReaderService


def read_included_files(local_repo_path: str) -> Dict[str, str]:
    include_files = input(
        "Do you want to include only specific files? "
        "If yes, write the file names separated by commas. If no, press enter.\n"
        "files: "
    )

    if include_files:
        print(f"Reading only files: {include_files}")

    include_files = include_files.split(",") if include_files else None

    contents = RepositoryReaderService().read_files(
        directory=local_repo_path, include_files=include_files
    )

    print(f"Read {len(contents)} files from {local_repo_path}")

    return contents

def run_code_writing_session(contents: Dict[str, str], local_repo_path: str):
    task = input("Please give me a task: ")
    coding_service = CodingService()
    coding_service.learn_code(file_abs_path_to_content=contents)
    code_feature_files = coding_service.code_feature(
        task=task, local_repo_path=local_repo_path
    )
    coding_service.write_code(
        coded_files=code_feature_files, local_repo_path=local_repo_path
    )

    print(f"Code written to {local_repo_path} successfully.")

def run_bug_finder_session(contents: Dict[str, str], local_repo_path: str):
    raise NotImplementedError


class MenuOption(BaseModel):
    option: str
    func: callable




def main():
    settings = get_settings()
    local_repo_path = settings.repo_path
    contents = read_included_files(local_repo_path=local_repo_path)

    menu_options: List[MenuOption] = [
        MenuOption(option="Code Writing", func=lambda: run_code_writing_session(
            contents=contents, local_repo_path=local_repo_path
        )),
        MenuOption(option="Bug Finder", func=lambda: run_bug_finder_session(
            contents=contents, local_repo_path=local_repo_path
        )),
    ]

    while True:
        print("Please choose an option:")

        for idx, option in enumerate(menu_options):
            print(f"{idx + 1}. {option.option}")

        choice = input("Choose an option: ")
        choice = int(choice)

        if choice not in range(1, len(menu_options) + 1):
            print("Invalid choice. Please try again.")
            continue

        menu_options[choice].func(contents=contents, local_repo_path=local_repo_path)

        continue_execution = input("Do you want to do something else? (yes/no) ")

        if continue_execution.lower() in ["no", "n"]:
            break
        else:
            print("Great! Let's do something else.")
            return


if __name__ == "__main__":
    main()
