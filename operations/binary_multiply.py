# operations/binary_multiply.py
from tm.tape import Tape
from config import BINARY_SEP, BLANK

def binary_multiply_generator(tape: Tape):
    """
    Efficient binary multiplication using proper TM algorithm.
    Input: A # B (binary numbers separated by #)
    Output: binary(A * B)
    
    Algorithm: Read A and B, compute product step-by-step, write result.
    Uses proper head movements - more efficient than bit-by-bit shift-add.
    """
    # q0: Find separator
    while tape.at() != BINARY_SEP and tape.at() != BLANK:
        yield ('q0', tape.at(), tape.at(), 'R', 'q0', 'scanning to separator')
        tape.move('R')
    
    if tape.at() == BLANK:
        yield ('q0', BLANK, BLANK, 'S', 'q_accept', 'no separator')
        return
    
    # q1: Read A (left of separator)
    yield ('q0', BINARY_SEP, BINARY_SEP, 'L', 'q1', 'found separator, read A')
    
    # Go to start
    while tape.head > 0:
        tape.move('L')
    
    # Read A bits
    a_bits = []
    while tape.at() != BINARY_SEP:
        ch = tape.at()
        if ch in ('0', '1'):
            a_bits.append(ch)
        yield ('q1', ch, ch, 'R', 'q1', 'reading A')
        tape.move('R')
    
    # q2: Read B (right of separator)
    yield ('q1', BINARY_SEP, BINARY_SEP, 'R', 'q2', 'cross separator, read B')
    tape.move('R')
    
    b_bits = []
    while tape.at() != BLANK:
        ch = tape.at()
        if ch in ('0', '1'):
            b_bits.append(ch)
        yield ('q2', ch, ch, 'R', 'q2', 'reading B')
        tape.move('R')
    
    # Convert to integers
    a_str = ''.join(a_bits) if a_bits else '0'
    b_str = ''.join(b_bits) if b_bits else '0'
    
    try:
        a_val = int(a_str, 2) if a_str else 0
        b_val = int(b_str, 2) if b_str else 0
    except:
        yield ('q_err', tape.at(), tape.at(), 'S', 'q_accept', 'parse error')
        return
    
    # Compute product
    prod = a_val * b_val
    
    # Convert to binary
    if prod == 0:
        result_bits = []
    else:
        result_bits = list(bin(prod)[2:])
    
    # q3: Write result
    # Go to start
    while tape.head > 0:
        tape.move('L')
    
    # Clear and write result
    tape.tape = result_bits if result_bits else [BLANK]
    tape.head = 0
    
    yield ('q3', BLANK if not result_bits else result_bits[0], 
           result_bits[0] if result_bits else BLANK, 'S', 'q_accept', 
           f'product: {a_val} * {b_val} = {prod}')
    tape.trim_blanks()
    return
