# Utilities imports

import re
from PySide2.QtWidgets import QMessageBox,QApplication
# allowed operators in a program
operators = [
    'x',
    '/',
    '+',
    '*',
    '^',
    '-'
]

# conversion string as input from user to mathematical function
replacements = {
    '^': '**',
    " ": "",
}


def validate_function(equation):
    # find all words and check if all are allowed:

    equation = equation.lower()
    for word in re.findall('[a-zA-Z_]+', equation):
        if word not in operators:
            print("55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")
            raise ValueError(
                f"Function of 'x' only allowed ,e.g: 5*x^3 + 2*x. \n Supported Operators: {', '.join(operators)}"
            )
    for old, new in replacements.items():
        equation = equation.replace(old, new)
    if "x" not in equation and equation != "":
        equation = f"{equation}+0*x"

    def func(x):
        try:
            return eval(equation)
        except Exception as e:
            return []

    return func


