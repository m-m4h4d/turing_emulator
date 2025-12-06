"""
Integration tests for the complete TM workflow.
Tests the full pipeline from input to output with transition tracking and halting.
"""
import unittest
from tm.simulator import TMSimulator
from tm.tape import Tape
from operations import build_initial_tape, get_generator_for
from config import MAX_STEPS


class TestIntegration(unittest.TestCase):
    """Integration tests for complete TM workflow."""

    def extract_unary_result(self, tape: Tape) -> int:
        """Extract integer result from unary tape."""
        content = tape.as_str()
        return content.count('1')

    def extract_binary_result(self, tape: Tape) -> int:
        """Extract integer result from binary tape."""
        content = tape.as_str()
        binary_str = ''.join(ch for ch in content if ch in ('0', '1'))
        if binary_str == '':
            return 0
        return int(binary_str, 2)

    def run_full_test(self, a: int, b: int, op: str, numeral: str, expected: int):
        """Run full test: execute operation, verify result, transition count, and halting."""
        # Build tape
        tape = build_initial_tape(a, b, numeral)
        initial_tape = tape.as_str()
        
        # Create generator
        gen = get_generator_for(op, numeral, tape)
        
        # Create simulator
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        # Track transitions
        transitions = []
        while not sim.is_halted():
            trans = sim.step()
            if trans is None:
                break
            transitions.append(trans)
        
        # Verify halting
        self.assertTrue(sim.is_halted(), 
                       f"Machine should halt for {op}({a}, {b}) in {numeral}")
        
        # Verify transition count
        self.assertGreater(sim.step_count, 0,
                          f"Should have at least one transition")
        self.assertLess(sim.step_count, MAX_STEPS,
                       f"Should complete within max steps")
        self.assertEqual(sim.step_count, len(transitions),
                        f"Step count should match number of transitions")
        
        # Verify result
        if numeral == 'unary':
            result = self.extract_unary_result(sim.tape)
        else:
            result = self.extract_binary_result(sim.tape)
        
        self.assertEqual(result, expected,
                       f"Result mismatch for {op}({a}, {b}) in {numeral}: "
                       f"expected {expected}, got {result}")
        
        return {
            'transitions': transitions,
            'step_count': sim.step_count,
            'result': result,
            'final_tape': sim.tape.as_str()
        }

    def test_integration_unary_add(self):
        """Full integration test for unary addition."""
        test_cases = [
            (2, 1, 3),
            (5, 3, 8),
            (0, 5, 5),
            (10, 0, 10),
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.run_full_test(a, b, 'add', 'unary', expected)

    def test_integration_unary_subtract(self):
        """Full integration test for unary subtraction."""
        test_cases = [
            (5, 2, 3),
            (10, 3, 7),
            (5, 5, 0),
            (2, 5, 0),  # Clamped to 0
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.run_full_test(a, b, 'subtract', 'unary', expected)

    def test_integration_unary_multiply(self):
        """Full integration test for unary multiplication."""
        test_cases = [
            (2, 3, 6),
            (3, 2, 6),
            (5, 0, 0),
            (0, 5, 0),
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.run_full_test(a, b, 'multiply', 'unary', expected)

    def test_integration_binary_add(self):
        """Full integration test for binary addition."""
        test_cases = [
            (3, 2, 5),
            (7, 5, 12),
            (0, 5, 5),
            (15, 7, 22),
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.run_full_test(a, b, 'add', 'binary', expected)

    def test_integration_binary_subtract(self):
        """Full integration test for binary subtraction."""
        test_cases = [
            (7, 3, 4),
            (10, 3, 7),
            (5, 5, 0),
            (3, 7, 0),  # Clamped to 0
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.run_full_test(a, b, 'subtract', 'binary', expected)

    def test_integration_binary_multiply(self):
        """Full integration test for binary multiplication."""
        test_cases = [
            (3, 2, 6),
            (4, 3, 12),
            (5, 0, 0),
            (7, 4, 28),
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.run_full_test(a, b, 'multiply', 'binary', expected)

    def test_transition_sequence_validity(self):
        """Test that transition sequence is valid."""
        tape = build_initial_tape(3, 2, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        transitions = []
        while not sim.is_halted():
            trans = sim.step()
            if trans is None:
                break
            transitions.append(trans)
        
        # Verify transitions have required fields
        for trans in transitions:
            self.assertIsNotNone(trans)
            self.assertEqual(len(trans), 6)  # (state, read, write, move, next_state, note)
            state, read, write, move, next_state, note = trans
            
            # States should be strings
            self.assertIsInstance(state, str)
            if next_state is not None:
                self.assertIsInstance(next_state, str)
            
            # Move should be valid if not None
            if move is not None:
                self.assertIn(move, ['L', 'R', 'S'])

    def test_tape_consistency(self):
        """Test that tape remains consistent throughout execution."""
        tape = build_initial_tape(5, 3, 'unary')
        initial_length = len(tape.tape)
        
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        # Track tape state
        tape_states = [tape.as_str()]
        
        while not sim.is_halted():
            sim.step()
            tape_states.append(tape.as_str())
        
        # Verify tape is never None
        for state in tape_states:
            self.assertIsNotNone(state)
        
        # Verify final tape is valid
        final_tape = sim.tape.as_str()
        self.assertIsNotNone(final_tape)
        self.assertIsInstance(final_tape, str)


if __name__ == '__main__':
    unittest.main()

