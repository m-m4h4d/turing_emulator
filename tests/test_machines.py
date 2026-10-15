"""
Tests for the transition-table machines in tm/machines.py.
Checks every machine against Python arithmetic over a range of inputs, and
checks that it halts in the accept state with only the result on the tape.
"""
import unittest
from tm import machines
from tm.machines import HALT, BLANK, get_machine, initial_tape, read_result, run
from tm.tape import Tape

EXPECTED = {
    'add': lambda a, b: a + b,
    'subtract': lambda a, b: max(a - b, 0),
    'multiply': lambda a, b: a * b,
}


def execute(machine, content, max_steps=200_000):
    tape = Tape(content)
    last = None
    steps = 0
    for last in run(machine, tape):
        steps += 1
        if steps >= max_steps:
            break
    return tape, last, steps


class TestMachines(unittest.TestCase):

    def check(self, op, numeral, operands):
        machine = get_machine(op, numeral)
        for a, b in operands:
            with self.subTest(op=op, numeral=numeral, a=a, b=b):
                tape, last, _ = execute(machine, initial_tape(a, b, numeral))
                self.assertEqual(last[4], HALT, f'did not accept; last transition {last}')
                self.assertEqual(read_result(tape.as_str(), numeral), EXPECTED[op](a, b))

    def test_unary_machines(self):
        pairs = [(a, b) for a in range(9) for b in range(9)]
        for op in EXPECTED:
            self.check(op, 'unary', pairs)

    def test_binary_machines(self):
        pairs = [(a, b) for a in range(33) for b in range(33)] + [(200, 200), (200, 1), (1, 200), (129, 127)]
        for op in EXPECTED:
            self.check(op, 'binary', pairs)

    def test_binary_result_has_no_leading_zeros(self):
        for op in EXPECTED:
            for a, b in [(5, 5), (8, 1), (0, 0), (12, 3)]:
                with self.subTest(op=op, a=a, b=b):
                    tape, _, _ = execute(get_machine(op, 'binary'), initial_tape(a, b, 'binary'))
                    digits = tape.as_str().strip(BLANK)
                    self.assertEqual(digits, bin(EXPECTED[op](a, b))[2:])

    def test_head_on_result_when_halted(self):
        for op in EXPECTED:
            for numeral in ('unary', 'binary'):
                with self.subTest(op=op, numeral=numeral):
                    tape, _, _ = execute(get_machine(op, numeral), initial_tape(6, 2, numeral))
                    self.assertEqual(tape.head, tape.leftmost_nonblank_index())

    def test_custom_unary_separator(self):
        for op, sep in (('add', '+'), ('subtract', '-'), ('multiply', '*')):
            machine = get_machine(op, 'unary', sep=sep)
            for a, b in [(0, 0), (3, 2), (2, 3), (4, 4)]:
                with self.subTest(op=op, a=a, b=b):
                    tape, last, _ = execute(machine, initial_tape(a, b, 'unary', sep=sep))
                    self.assertEqual(last[4], HALT)
                    self.assertEqual(read_result(tape.as_str(), 'unary'), EXPECTED[op](a, b))

    def test_stuck_machine_reports_no_next_state(self):
        machine = get_machine('add', 'unary')
        tape, last, steps = execute(machine, '1#1')  # '#' is not in this machine's alphabet
        self.assertEqual(steps, 2)
        self.assertIsNone(last[4])

    def test_rules_only_use_known_states(self):
        for op in EXPECTED:
            for numeral in ('unary', 'binary'):
                machine = get_machine(op, numeral)
                with self.subTest(op=op, numeral=numeral):
                    sources = {state for state, _ in machine.rules}
                    for _, _, _, move, next_state, _ in machine.table():
                        self.assertIn(move, ('L', 'R', 'S'))
                        self.assertTrue(next_state == HALT or next_state in sources,
                                        f'{next_state} has no rules')
                    self.assertNotIn(HALT, sources)

    def test_duplicate_rule_rejected(self):
        m = machines.Machine('dup')
        m.add('q0', '1', None, 'R', 'q0')
        with self.assertRaises(ValueError):
            m.add('q0', '01', None, 'R', 'q0')


if __name__ == '__main__':
    unittest.main()
