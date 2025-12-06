# operations/binary_subtract.py
from tm.tape import Tape
from config import BLANK, BINARY_SEP

def binary_subtract_generator(tape: Tape):
    """
    Binary subtraction (a - b) with borrow; clamp to 0 if negative.
    This mirrors the structure of binary_add_generator but computes difference.
    """
    borrow = 0
    # go to rightmost blank
    while tape.at() != BLANK:
        yield ('bs_scan', tape.at(), tape.at(), 'R', 'bs_scan', 'scan right end')
        tape.move('R')
    tape.move('L')
    yield ('bs_start', tape.at(), tape.at(), 'S', 'bs_loop', 'start from rightmost')
    while True:
        b_ch = tape.at()
        if b_ch == BINARY_SEP:
            left_exists = any(ch in ('0','1') for ch in tape.tape[:tape.head])
            if not left_exists:
                if borrow == 1:
                    tape.tape = [BLANK]
                    tape.head = 0
                    yield ('bs_neg', BLANK, BLANK, 'S', 'q_accept', 'negative -> clamp to 0')
                    return
                else:
                    yield ('bs_done', tape.at(), tape.at(), 'S', 'q_accept', 'done no borrow')
                    break
            b = 0
            tape.move('L')
            yield ('bs_proc', BINARY_SEP, BINARY_SEP, 'L', 'bs_proc', 'sep->treat b=0')
        else:
            b = 1 if b_ch == '1' else 0
            tape.move('L')
            yield ('bs_proc', b_ch, b_ch, 'L', 'bs_proc', 'read b and go left')

        # find separator and read a
        while tape.head >= 0 and tape.at() != BINARY_SEP:
            yield ('bs_cross', tape.at(), tape.at(), 'L', 'bs_cross', 'move left to sep')
            tape.move('L')
        if tape.at() == BINARY_SEP:
            tape.move('L')
            yield ('bs_cross', BINARY_SEP, BINARY_SEP, 'L', 'bs_cross', 'crossed sep')
        a_ch = tape.at()
        a = 1 if a_ch == '1' else 0 if a_ch == '0' else 0

        diff = a - b - borrow
        if diff >= 0:
            out = diff
            borrow = 0
        else:
            out = diff + 2
            borrow = 1

        # write out into B region
        while tape.at() != BINARY_SEP:
            yield ('bs_toB', tape.at(), tape.at(), 'R', 'bs_toB', 'move right to sep')
            tape.move('R')
        tape.move('R')
        tape.write('1' if out == 1 else '0')
        yield ('bs_write', b_ch, '1' if out == 1 else '0', 'S', 'bs_written', f'write diff bit {out}')
        tape.move('L')
        tape.move('L')

        # reposition to right end for next iter
        while tape.at() != BLANK:
            yield ('bs_repos', tape.at(), tape.at(), 'R', 'bs_repos', 'advance to right end')
            tape.move('R')
        tape.move('L')
        yield ('bs_repos', tape.at(), tape.at(), 'S', 'bs_next', 'repositioned')

    # finalize
    if borrow == 1:
        tape.tape = [BLANK]
        tape.head = 0
        yield ('bs_final_neg', BLANK, BLANK, 'S', 'q_accept', 'final borrow -> negative -> clamp')
    else:
        # strip leading zeros
        r_end = tape.rightmost_nonblank_index()
        leftmost = None
        for i in range(r_end+1):
            if tape.tape[i] in ('0','1'):
                leftmost = i
                break
        if leftmost is None:
            tape.tape = [BLANK]
            tape.head = 0
            yield ('bs_done_zero', BLANK, BLANK, 'S', 'q_accept', 'result zero')
        else:
            while leftmost <= r_end and tape.tape[leftmost] == '0':
                leftmost += 1
            if leftmost > r_end:
                tape.tape = [BLANK]
                tape.head = 0
            else:
                tape.tape = tape.tape[leftmost:r_end+1]
                tape.head = 0
            yield ('bs_done', tape.at(), tape.at(), 'S', 'q_accept', 'done and normalized')
    tape.trim_blanks()
    return
