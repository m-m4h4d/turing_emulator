# config.py
# Global configuration / defaults used across the project.

# Tape symbols are defined with the machines: blank '_', unary separator '0',
# binary separator '#' (distinct from the '0' digit).
from tm.machines import BLANK, UNARY_SEP, BINARY_SEP
MAX_STEPS = 100_000
INPUT_LIMIT = 200    # max a,b (in magnitude/length) by default
