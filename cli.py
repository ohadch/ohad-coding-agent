import glob
import json

from dotenv import load_dotenv

load_dotenv()

import os
from dataclasses import dataclass

from typing import Dict, List

from src import get_settings

from src.services.coding_service import CodingService
from src.services.repository_reader_service import RepositoryReaderService


def read_included_files(local_repo_path: str) -> Dict[str, str]:
    # Ask the user if he would like to provide glob pattern or specific files
    response = input(
        # "Do you want to include only specific files? "
        # "If yes, please choose a way to include files: "
        # "1. Glob pattern\n"
        # "2. Specific files\n"
        f"""Do you want to include only specific files?
        If yes, please choose a way to include files:
        0. Glob pattern
        1. Specific files
        2. Read all files
        """
    )

    if response == "0":
        include_files_glob = input(
            "Please provide a glob pattern to include files: "
        )

        glob_pattern = os.path.join(local_repo_path, include_files_glob)
        print(f"Using glob pattern: {glob_pattern}")
        include_files = glob.glob(glob_pattern, recursive=True)
        include_files = list(set([os.path.basename(file) for file in include_files]))
    elif response == "1":
        include_files = input(
            "Do you want to include only specific files? "
            "If yes, write the file names separated by commas. If no, press enter.\n"
            "files: "
        )
        include_files = include_files.split(",")
    else:
        include_files = None

    contents = RepositoryReaderService().read_files(
        directory=local_repo_path,
        include_files=include_files
    )

    print(f"Read {len(contents)} files from {local_repo_path}")

    return contents


def run_code_writing_session(local_repo_path: str):
    contents = read_included_files(local_repo_path=local_repo_path)
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


def run_bug_finder_session(local_repo_path: str):
    contents = read_included_files(local_repo_path=local_repo_path)
    bugs_output_dir = os.path.join(local_repo_path, "ohad_bugs")

    for idx, (file_path, content) in enumerate(contents.items()):
        print(f"Reviewing file {idx + 1}/{len(contents)}: {file_path}")
        coding_service = CodingService()
        coding_service.learn_code(file_abs_path_to_content={file_path: content})
        response = coding_service.find_bugs()
        bugs_found = response["bugs_found"]
        bugs = response["issues"]

        if bugs_found and bugs:
            print(f"Found {len(bugs)} bugs in {file_path}")
            os.makedirs(bugs_output_dir, exist_ok=True)
            output_file_path = os.path.join(bugs_output_dir, f"{os.path.basename(file_path)}.bugs.json")
            with open(output_file_path, "w") as f:
                print(f"Writing bugs to {output_file_path}")
                f.write(json.dumps(bugs, indent=4))



@dataclass
class MenuOption:
    option: str
    func: callable


def main():
    settings = get_settings()
    local_repo_path = settings.repo_path
    menu_options: List[MenuOption] = [
        MenuOption(
            option="Code Writing",
            func=lambda: run_code_writing_session(
                local_repo_path=local_repo_path
            )
        ),
        MenuOption(
            option="Bug Finder",
            func=lambda: run_bug_finder_session(
                local_repo_path=local_repo_path
            )
        ),
    ]

    while True:
        print("Please choose an option:")

        for idx, option in enumerate(menu_options):
            print(f"{idx}. {option.option}")

        choice = input("Choose an option: ")
        choice = int(choice)

        menu_options[choice].func()

        continue_execution = input("Do you want to do something else? (yes/no) ")

        if continue_execution.lower() in ["no", "n"]:
            break
        else:
            print("Great! Let's do something else.")
            return


if __name__ == "__main__":
    main()
