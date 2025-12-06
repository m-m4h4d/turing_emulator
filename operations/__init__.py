# operations/__init__.py
from typing import Generator
from tm.tape import Tape
from operations import unary_add, unary_subtract, unary_multiply
from operations import binary_add, binary_subtract, binary_multiply

def build_initial_tape(a: int, b: int, numeral: str = 'unary', blank: str = None) -> Tape:
    """
    Build an initial tape for given operands and numeral system.
    For unary: '1'*a + UNARY_SEP + '1'*b
    For binary: binary(a) + BINARY_SEP + binary(b)
    """
    from config import UNARY_SEP, BINARY_SEP, BLANK, INPUT_LIMIT
    if blank is None:
        blank = BLANK
    # input bounds enforced lightly here
    if a < 0 or b < 0:
        raise ValueError("Only non-negative integers allowed.")
    if a > INPUT_LIMIT or b > INPUT_LIMIT:
        raise ValueError(f"Inputs limited to {INPUT_LIMIT} for safety.")
    if numeral == 'unary':
        left = '1' * a if a > 0 else ''
        right = '1' * b if b > 0 else ''
        content = left + UNARY_SEP + right
        return Tape(content=content, blank=blank)
    elif numeral == 'binary':
        left = bin(a)[2:] if a > 0 else ''
        right = bin(b)[2:] if b > 0 else ''
        content = left + BINARY_SEP + right
        return Tape(content=content, blank=blank)
    else:
        raise ValueError("Unknown numeral system")

def get_generator_for(operation: str, numeral: str, tape: Tape) -> Generator:
    op = operation.lower()
    if numeral == 'unary':
        if op == 'add':
            return unary_add.unary_add_generator(tape)
        if op == 'subtract':
            return unary_subtract.unary_subtract_generator(tape)
        if op == 'multiply':
            return unary_multiply.unary_multiply_generator(tape)
    elif numeral == 'binary':
        if op == 'add':
            return binary_add.binary_add_generator(tape)
        if op == 'subtract':
            return binary_subtract.binary_subtract_generator(tape)
        if op == 'multiply':
            return binary_multiply.binary_multiply_generator(tape)
    raise ValueError("Unsupported op/numeral combo")
