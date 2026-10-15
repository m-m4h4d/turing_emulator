# operations/__init__.py
# Builds input tapes and runs the transition-table machines from tm/machines.py.
from typing import Generator
from tm.tape import Tape
from tm import machines


def build_initial_tape(a: int, b: int, numeral: str = 'unary', blank: str = None) -> Tape:
    """
    Build an initial tape for given operands and numeral system.
    For unary: '1'*a + UNARY_SEP + '1'*b
    For binary: binary(a) + BINARY_SEP + binary(b)
    """
    from config import BLANK, INPUT_LIMIT
    if blank is None:
        blank = BLANK
    if a > INPUT_LIMIT or b > INPUT_LIMIT:
        raise ValueError(f"Inputs limited to {INPUT_LIMIT} for safety.")
    return Tape(content=machines.initial_tape(a, b, numeral), blank=blank)


def get_generator_for(operation: str, numeral: str, tape: Tape) -> Generator:
    """Run the machine for operation/numeral on tape, yielding one transition per step."""
    return machines.run(machines.get_machine(operation, numeral), tape)
