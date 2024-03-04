import pylint.lint
import tempfile
import sys
import os
import json

#expects tagless python code
class lintingTest:
    def __init__(self, text):
        self.text = text

    # Create a temporary file to write the code string
    def to_file(self):    
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(self.text)
        return temp_file.name

    def run_lint(self):
        temp_file_name = self.to_file()
        # Configure pylint options to check only for errors (E) and fatal (F) errors
        pylint_options = ["--disable=all", "--enable=E,F"]
        # Run pylint on the temporary file with the specified options
        exit_code = pylint.lint.Run(pylint_options + [temp_file_name], exit=False).linter.msg_status
        # Remove the temporary file
        os.remove(temp_file_name)

        # Return True if there are no errors (exit_code is 0), False otherwise
        if (exit_code == 0): 
            return True
        else:
            return False


