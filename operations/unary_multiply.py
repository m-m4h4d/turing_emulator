# operations/unary_multiply.py
from tm.tape import Tape
from config import UNARY_SEP, BLANK

def unary_multiply_generator(tape: Tape):
    """
    Efficient unary multiplication - simplified algorithm.
    Input: A 0 B (e.g., 1110111 = 3 * 3)
    Output: 1^(a*b)
    
    Algorithm: Count A and B, then write a*b ones.
    More efficient than copying A for each B.
    """
    # q0: Find separator and count A
    a_count = 0
    while True:
        r = tape.at()
        if r == UNARY_SEP:
            yield ('q0', r, r, 'R', 'q1', 'found separator')
            tape.move('R')
            break
        elif r == '1':
            a_count += 1
            yield ('q0', r, r, 'R', 'q0', 'counting A')
            tape.move('R')
        elif r == BLANK:
            yield ('q0', r, r, 'S', 'q_accept', 'no separator - result is 0')
            return
        else:
            yield ('q0', r, r, 'R', 'q0', 'scanning')
            tape.move('R')
    
    # q1: Count B
    b_count = 0
    while tape.at() != BLANK:
        r = tape.at()
        if r == '1':
            b_count += 1
        yield ('q1', r, r, 'R', 'q1', 'counting B')
        tape.move('R')
    
    # Compute result
    result_count = a_count * b_count
    
    # q2: Write result
    # Go to start
    while tape.head > 0:
        tape.move('L')
    
    # Clear tape and write result
    if result_count == 0:
        tape.tape = [BLANK]
    else:
        tape.tape = ['1'] * result_count
    tape.head = 0
    
    yield ('q2', BLANK, '1' if result_count > 0 else BLANK, 'S', 'q_accept', 
           f'multiplication complete: {a_count} * {b_count} = {result_count}')
    tape.trim_blanks()
    return
