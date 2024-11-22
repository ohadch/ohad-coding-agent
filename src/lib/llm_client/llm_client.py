import abc
import json
import logging
from typing import Dict, List

from src.types.schema import LlmMessage
from src.utils.exceptions import BadLlmResponseError


class LlMClient(abc.ABC):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._memory: List[LlmMessage] = []


    def init_configuration(self):
        init_response = self._send_json_message(f"""
                From now on, respond with jsons of the following format:
                {{
                    success: bool,
                    message: str
                }}
                Do not respond with anything else.
                If you understand, then respond with:
                {{
                    success: true,
                    message: "I understand"
                }}
                """)

        if not init_response["success"]:
            raise BadLlmResponseError(f"Could not initialize the llm: {init_response['message']}")

        return init_response

    def teach_code(self, file_abs_path_to_content: Dict[str, str]):
        self.init_configuration()

        # Tell the llm that we are now going to teach it code from our repository.
        # From the next message on, we are going to send each file in the following format:
        # {{ file_abs_path: str, content: str }}
        # After each file, the model should respond with:
        # {{ success: bool, message: learned the file at THE_FILE_ABS_PATH successfully }}
        # When we are done, we will send:
        # FINISHED_TEACHING
        # Then, the model should respond with:
        # {{ success: bool, message: "I learned all the code you taught me" }}
        for file_abs_path, content in file_abs_path_to_content.items():
            self._logger.info(f"Teaching the llm the file at {file_abs_path}")
            teach_file_response = self._send_json_message(f"""
                {{
                    file_abs_path: "{file_abs_path}",
                    content: "{content}"
                }}
                """)
            if not teach_file_response["success"]:
                raise BadLlmResponseError(f"Could not teach the llm: {teach_file_response['message']}")

            if teach_file_response["message"] != f"learned the file at {file_abs_path} successfully":
                raise BadLlmResponseError(f"Could not teach the llm: {teach_file_response['message']}")

        finished_teaching_response = self._send_json_message("FINISHED_TEACHING")
        if not finished_teaching_response["success"]:
            raise BadLlmResponseError(f"Could not teach the llm: {finished_teaching_response['message']}")

        if finished_teaching_response["message"] != "I learned all the code you taught me":
            raise BadLlmResponseError(f"Could not teach the llm: {finished_teaching_response['message']}")

        self._logger.info("Finished teaching the llm")

        return finished_teaching_response

    def _send_json_message(self, message: str, **kwargs) -> Dict:
        response = self.send_message(message, **kwargs)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            self._logger.error(f"Could not parse response as json: {response}")
            raise

    def reset_memory(self):
        self._memory = []
        self._logger.info("Memory reset successfully")

    def send_message(self, message: str, role: str = "user", **kwargs) -> str:
        user_message = LlmMessage(
            role=role,
            content=message
        )

        response = self._send_message_implementation_specific_logic(
            message=user_message,
            **kwargs
        )

        self._memory.extend([
            user_message,
            response
        ])

        return response.content

    @abc.abstractmethod
    def _send_message_implementation_specific_logic(self, message: LlmMessage, **kwargs) -> LlmMessage:
        pass