import os
import sys

class HousingException(Exception):

    def __init__(self, error_message:Exception, error_detail:sys):
        # super.__init__(error_message)
        self.error_message = HousingException.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_detail:sys)->str:
        """
        error_message: Exception object
        error_detail: Object of sys module
        """
        _, _, exec_tb = error_detail.exc_info()
        exception_line_no = exec_tb.tb_frame.f_lineno
        try_line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"""[Script {file_name}:\n 
        Error occured at try block {try_line_number}, exception block {exception_line_no},\n 
        error message: {error_message}]"""
        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return HousingException.__name__.str()