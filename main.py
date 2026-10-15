# main.py
import argparse
from operations import build_initial_tape, get_generator_for
from tm.machines import HALT, get_machine, read_result
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
    if not sim.last_transition or sim.last_transition[4] != HALT:
        print("Machine did not reach the accept state (stuck or step limit); no result.")
        return
    print(f"Result ({numeral} -> int):", read_result(sim.tape.as_str(), numeral))

def print_table(args):
    m = get_machine(args.op, args.numeral)
    print(f"{m.name}: start state {m.start}, {len(m.states())} states, {len(m.rules)} rules")
    print(f"{'state':<16} {'read':<5} {'write':<6} {'move':<5} {'next':<16} note")
    for state, read, write, move, next_state, note in m.table():
        print(f"{state:<16} {read:<5} {write:<6} {move:<5} {next_state:<16} {note}")

def main():
    parser = argparse.ArgumentParser(description="Turing Machine Emulator (Arithmetic)")
    parser.add_argument('--cli', action='store_true', help='run in CLI mode')
    parser.add_argument('--table', action='store_true', help='print the transition table for --op/--numeral')
    parser.add_argument('--op', default='add', choices=['add','subtract','multiply'], help='operation')
    parser.add_argument('--numeral', default='unary', choices=['unary','binary'], help='numeral system')
    parser.add_argument('--a', type=int, default=3, help='operand a (non-negative int)')
    parser.add_argument('--b', type=int, default=2, help='operand b (non-negative int)')
    args = parser.parse_args()

    if args.table:
        print_table(args)
        return
    if args.cli:
        cli_mode(args)
        return

    import tkinter as tk
    from ui.gui import TMGUI
    root = tk.Tk()
    app = TMGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
