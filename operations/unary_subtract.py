# operations/unary_subtract.py
from tm.tape import Tape
from config import UNARY_SEP, BLANK

def unary_subtract_generator(tape: Tape):
    """
    Unary subtraction: produce a-b clamped to 0.
    Algorithm:
      - For each '1' in right operand, cross one '1' in left operand.
      - If left runs out -> produce blank (0)
      - Else cleanup markers and result remains in left.
    Markers used: X (used on right), Y (used on left)
    """
    # go to separator
    state = 'q0'
    while True:
        r = tape.at()
        if r == UNARY_SEP:
            yield (state, r, r, 'R', 'q1', 'found separator')
            tape.move('R')
            state = 'q1'
            break
        elif r == BLANK:
            yield (state, r, r, 'S', 'q_accept', 'no separator - halt')
            return
        else:
            yield (state, r, r, 'R', state, 'scanning left number')
            tape.move('R')

    # main loop: for each unmarked '1' in right, find a left '1' and mark it
    while True:
        r = tape.at()
        if r == '1':
            tape.write('X')  # mark right 1
            yield ('q1', '1', 'X', 'L', 'q2', 'mark right 1 as X')
            tape.move('L')
            # move left to separator
            while tape.at() != UNARY_SEP:
                yield ('q2', tape.at(), tape.at(), 'L', 'q2', 'moving left to separator')
                tape.move('L')
            # cross sep
            yield ('q2', tape.at(), tape.at(), 'L', 'q3', 'cross separator to left')
            tape.move('L')
            # find a left '1' to erase (mark Y)
            found_left = False
            while True:
                ch = tape.at()
                if ch == '1':
                    tape.write('Y')
                    yield ('q3', '1', 'Y', 'R', 'q4', 'mark left 1 as Y (erased)')
                    tape.move('R')
                    found_left = True
                    break
                elif ch == 'Y':
                    yield ('q3', 'Y', 'Y', 'L', 'q3', 'skip Y')
                    tape.move('L')
                elif ch == BLANK:
                    # no left ones left -> clamp to 0
                    yield ('q3', BLANK, BLANK, 'R', 'q5', 'no left ones - clamp to 0')
                    tape.move('R')
                    break
                else:
                    yield ('q3', ch, ch, 'L', 'q3', 'search left 1')
                    tape.move('L')
            if not found_left:
                state = 'q5'
                break
            # return to right area
            while True:
                ch = tape.at()
                if ch == UNARY_SEP:
                    yield ('q4', ch, ch, 'R', 'q1', 'back at separator - resume')
                    tape.move('R')
                    state = 'q1'
                    break
                else:
                    yield ('q4', ch, ch, 'R', 'q4', 'moving right to separator')
                    tape.move('R')
            continue
        elif r == 'X':
            yield ('q1', 'X', 'X', 'R', 'q1', 'skip marked right')
            tape.move('R')
            continue
        elif r == BLANK:
            yield ('q1', BLANK, BLANK, 'L', 'q5', 'finished processing right ones; cleanup')
            state = 'q5'
            break
        else:
            yield ('q1', r, r, 'R', 'q1', 'scanning right')
            tape.move('R')

    # cleanup: remove X,Y and separator; if we detected left empty earlier, result becomes blank
    while tape.at() != BLANK:
        ch = tape.at()
        if ch in ('X', 'Y', UNARY_SEP):
            tape.write(BLANK)
            yield ('q5', ch, BLANK, 'R', 'q5', 'erasing markers/separator')
            tape.move('R')
        else:
            yield ('q5', ch, ch, 'R', 'q5', 'skip')
            tape.move('R')
    # finalize by removing remaining Ys if any and trimming
    for i in range(len(tape.tape)):
        if tape.tape[i] == 'Y':
            tape.tape[i] = BLANK
    tape.trim_blanks()
    yield ('q6', tape.at(), tape.at(), 'S', 'q_accept', 'cleanup done; halt')
    return
