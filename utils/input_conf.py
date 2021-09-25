
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
    Return: int
    -----------------------------------
    return the new one (initial_value if it has not changed)

    """
    value = initial_value
    while not function(value):
        print(f"{label} not valid")
        value = input(f"{label}({status}): ")

    return value
