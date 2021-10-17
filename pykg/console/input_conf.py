from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import string
from regex.data_re import REGEX_EMAIL, REGEX_GIT_PROJECT, REGEX_VERSION_NUMBER
from regex.file_re import REGEX_FILE_PY
import re


def get_style():
    return style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })


def validate(label, function, status, initial_value):
    """
    this function validates a string
    --------------------------------
    label: str
        the input label
    function: fun
        the code will start over as long as function (value) is equal to True
    status: str
        the status of the input
        choices: optional, required, default =
    initial_value: str
        initial user input
    -----------------------------------
    Return: str
    -----------------------------------
    return the new one (initial_value if it has not changed)
    """
    value = initial_value
    is_optional = status == "optionel" or status == "default=1.0.0"
    if is_optional:
        bool_opt = lambda v: v != ''
    else:
        bool_opt = lambda v: True
    while not function(value) and bool_opt(value):
        print(f"{label} not valid")
        value = input(f"{label}({status}): ")

    return value


class InputStyle:
    style = get_style()
    form = []

    def render(self):
        return prompt(self.form, style=self.style)


class ValidateRequired(Validator):

    def validate(self):
        document = self

        if not bool(document.text):
            raise ValidationError(
                message=f"is required",
                cursor_position=len(self.text)
            )


class ValidateOptionel(Validator):

    def validate(self, **kwargs):
        document = self
        if bool(document.text):
            if not all([i in string.ascii_letters + string.digits for i in document.text]):
                raise ValidationError(
                    message=f"{document.text} is bad format",
                    cursor_position=len(document.text)
                )


class ValidateEmail(Validator):

    def validate(self):
        document = self
        if bool(document.text):
            if not re.match(REGEX_EMAIL, document.text):
                raise ValidationError(
                    message=f"{document.text} is bad format(format do be email)",
                    cursor_position=len(document.text)
                )


class ValidateGit(Validator):

    def validate(self):
        document = self

        if bool(document.text):
            if not re.match(REGEX_GIT_PROJECT, document.text):
                raise ValidationError(
                    message=f"{document.text} is bad format(format do be git project)",
                    cursor_position=len(document.text)
                )


class ValidateVersion(Validator):

    def validate(self):
        document = self
        if bool(document.text):
            if not re.match(REGEX_VERSION_NUMBER, document.text):
                raise ValidationError(
                    message=f"{document.text} is bad format(format do be version)",
                    cursor_position=len(document.text)
                )


class ValidateFilePy(Validator):

    def validate(self):
        document = self
        if bool(document.text):
            if not re.match(REGEX_FILE_PY, document.text):
                raise ValidationError(
                    message=f"{document.text} is bad format(format do be file py)",
                    cursor_position=len(document.text)
                )