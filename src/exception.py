from src.logger import logging
import sys


def error_message_detail(error, error_detial: sys):
    """
        error_message: str - Description of the error
        error_detail: sys - System details of the error (like traceback info)
    """
    # Extract detailed error info (file name, line number)
    _, _, exc_tb = error_detial.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomExcption(Exception):
    """A custom exception class to handle and log errors in the project."""

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detial=error_detail)

    def __str__(self):
        return self.error_message
