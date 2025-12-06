# main.py
import argparse
import sys
import tkinter as tk
from ui.gui import TMGUI
from operations import build_initial_tape, get_generator_for
from tm.simulator import TMSimulator
from tm.tape import Tape
from config import MAX_STEPS

def cli_mode(args):
    numeral = args.numeral
    op = args.op
    a = args.a
    b = args.b
    try:
        tape = build_initial_tape(a,b,numeral)
    except Exception as ex:
        print("Input validation error:", ex)
        return
    gen = get_generator_for(op, numeral, tape)
    sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
    print(f"Initial tape: {tape.as_str()}, head={tape.head}")
    while not sim.is_halted():
        trans = sim.step()
        if trans is None:
            break
        state, read, write, move, next_state, note = trans
        print(f"Step {sim.step_count}: ({state}, {read}) -> ({write}, {move}, {next_state}) [{note}]")
    print("Final tape:", sim.tape.as_str())
    # present result
    if numeral == 'unary':
        res = sim.tape.as_str().count('1')
        print("Result (unary -> int):", res)
    else:
        s = ''.join(ch for ch in sim.tape.tape if ch in ('0','1'))
        if s == '':
            print("Result (binary -> int): 0 (blank)")
        else:
            print("Result (binary -> int):", int(s,2))

def main():
    parser = argparse.ArgumentParser(description="Turing Machine Emulator (Arithmetic)")
    parser.add_argument('--cli', action='store_true', help='run in CLI mode')
    parser.add_argument('--op', default='add', choices=['add','subtract','multiply'], help='operation')
    parser.add_argument('--numeral', default='unary', choices=['unary','binary'], help='numeral system')
    parser.add_argument('--a', type=int, default=3, help='operand a (non-negative int)')
    parser.add_argument('--b', type=int, default=2, help='operand b (non-negative int)')
    args = parser.parse_args()

    if args.cli:
        cli_mode(args)
        return

    root = tk.Tk()
    app = TMGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
