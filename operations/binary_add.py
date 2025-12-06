# operations/binary_add.py
from tm.tape import Tape
from config import BLANK, BINARY_SEP

def binary_add_generator(tape: Tape):
    """
    Binary addition (pragmatic single-tape algorithm).
    This implementation walks to the right end and then performs addition right-to-left,
    writing the result into the B region. It yields transitions for UI/logging.
    """
    carry = 0
    # go to rightmost blank
    while tape.at() != BLANK:
        yield ('scan_right', tape.at(), tape.at(), 'R', 'scan_right', 'advance to right blank')
        tape.move('R')
    # step to last bit
    tape.move('L')
    yield ('start', tape.at(), tape.at(), 'S', 'process', 'start from rightmost')
    while True:
        b_ch = tape.at()
        if b_ch == BINARY_SEP:
            # treat b = 0 and check finish condition
            left_exists = any(ch in ('0','1') for ch in tape.tape[:tape.head])
            if not left_exists and carry == 0:
                yield ('finish', tape.at(), tape.at(), 'S', 'q_accept', 'done - no carry and no bits left')
                break
            b = 0
            yield ('proc_sep', BINARY_SEP, BINARY_SEP, 'L', 'proc_left', 'sep encountered; b=0')
            tape.move('L')
        else:
            b = 1 if b_ch == '1' else 0
            tape.move('L')
            yield ('proc_b', b_ch, b_ch, 'L', 'to_a', 'read b and move to A')

        # move left until separator
        while tape.head >= 0 and tape.at() != BINARY_SEP:
            yield ('seek_sep', tape.at(), tape.at(), 'L', 'seek_sep', 'seeking sep')
            tape.move('L')
        if tape.at() == BINARY_SEP:
            tape.move('L')
            yield ('cross', BINARY_SEP, BINARY_SEP, 'L', 'read_a', 'crossed sep')
        a_ch = tape.at()
        a = 1 if a_ch == '1' else 0
        s = (a + b + carry) % 2
        new_carry = 1 if (a + b + carry) >= 2 else 0

        # move right to B region for writing
        while tape.at() != BINARY_SEP:
            yield ('to_b', tape.at(), tape.at(), 'R', 'to_b', 'move to sep')
            tape.move('R')
        tape.move('R')  # go into B region
        write_char = '1' if s == 1 else '0'
        tape.write(write_char)
        yield ('write', b_ch, write_char, 'S', 'written', f'write sum bit {write_char} carry was {carry}')

        # set carry and reposition for next
        carry = new_carry
        tape.move('L')
        tape.move('L')

        left_exists = any(ch in ('0','1') for ch in tape.tape[:tape.head+1])
        if not left_exists and carry == 0:
            yield ('maybe_finish', tape.at(), tape.at(), 'S', 'q_accept', 'done')
            break
        # reposition to rightmost nonblank
        while tape.at() != BLANK:
            yield ('repos_right', tape.at(), tape.at(), 'R', 'repos', 'move right to blank')
            tape.move('R')
        tape.move('L')
        yield ('repos_done', tape.at(), tape.at(), 'S', 'next', 'repositioned')

    # final carry
    if carry == 1:
        tape.move('L')
        tape.write('1')
        yield ('final_carry', BLANK, '1', 'S', 'q_accept', 'write final carry')
    tape.trim_blanks()
    return
