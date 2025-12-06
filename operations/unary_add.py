# operations/unary_add.py
from tm.tape import Tape
from config import UNARY_SEP, BLANK

def unary_add_generator(tape: Tape):
    """
    Unary Addition Turing Machine - Optimized
    Input: 111011 -> 3 + 2
    Output: 11111
    Algorithm: Remove the separator by shifting all '1's after it left.
    """
    # q0: scan to separator
    while True:
        r = tape.at()
        if r == UNARY_SEP:
            yield ('q0', r, BLANK, 'R', 'q1', 'found separator, remove it')
            tape.write(BLANK)
            # We're now at the position after the blank (first char of right operand)
            break
        elif r == BLANK:
            yield ('q0', r, r, 'S', 'q_accept', 'no separator - halt')
            return
        else:
            yield ('q0', r, r, 'R', 'q0', 'scanning left number')
            tape.move('R')
    
    # q1: shift all '1's after the blank left to fill it
    # We're at the position after the blank (first char of right operand)
    # Move back to the blank
    tape.move('L')
    # Now move right to first character to shift
    tape.move('R')
    ch = tape.at()
    yield ('q1', ch, ch, 'S', 'q1', 'starting shift')
    
    shift_count = 0
    while True:
        ch = tape.at()
        
        if ch == BLANK:
            # End of tape, done shifting
            if shift_count > 0:
                tape.move('L')  # Move back to last shifted '1'
            break
        elif ch == '1':
            # Copy this '1' to previous position (the blank)
            tape.move('L')
            tape.write('1')
            shift_count += 1
            yield ('q1', '1', '1', 'R', 'q1', f'shifting 1 left ({shift_count})')
            tape.move('R')  # Back to where we were reading
            # Now move to next position
            tape.move('R')
        else:
            # Skip unexpected characters
            tape.move('R')
    
    # Clear any remaining '1's that weren't shifted (duplicates)
    if shift_count > 0:
        tape.move('R')
        if tape.at() == '1':
            # This is a duplicate, clear it
            tape.write(BLANK)
            yield ('q1', '1', BLANK, 'L', 'q2', 'clearing duplicate')
            tape.move('L')
        else:
            tape.move('L')
    
    # Move to start and compact by removing middle blanks
    while tape.head > 0:
        tape.move('L')
    
    # Compact: remove any blanks in the middle by shifting
    # Go through tape and shift all '1's left, skipping blanks
    write_pos = 0
    read_pos = 0
    
    # Find first '1'
    while read_pos < len(tape.tape) and tape.tape[read_pos] != '1':
        read_pos += 1
    
    # Copy all '1's, skipping blanks
    while read_pos < len(tape.tape):
        if tape.tape[read_pos] == '1':
            if read_pos != write_pos:
                tape.tape[write_pos] = '1'
            write_pos += 1
        read_pos += 1
    
    # Clear remaining positions
    while write_pos < len(tape.tape):
        tape.tape[write_pos] = BLANK
        write_pos += 1
    
    # Update head
    tape.head = 0
    while tape.head < len(tape.tape) and tape.at() == BLANK:
        tape.head += 1
    if tape.head >= len(tape.tape):
        tape.head = 0
    
    # Final cleanup - trim blanks
    tape.trim_blanks()
    yield ('q_accept', tape.at(), tape.at(), 'S', 'q_accept', 'addition complete')
    return
