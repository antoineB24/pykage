from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
import string
from .regex import REGEX_EMAIL, REGEX_GIT_PROJECT, REGEX_VERSION_NUMBER, REGEX_FILE_PY
import re



def get_style():
    return Style.from_dict({
        'question': '#0348FF bold',
        'responce': '#03A0FF'
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
    res = type('Res', (), {})

    def add_question(self, name, label, validate: Validator):
        self.form.append({'name': name,
                          'question': HTML(f'<question>{label}</question>'),
                          'responce': '',
                          'validate' : validate
                          })

    def render(self):

        for i in self.form:
            i["responce"] = prompt(i["question"], style=self.style, validator=i["validator"])
            setattr(self.res, i["name"], i["responce"])




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
