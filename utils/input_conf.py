
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
