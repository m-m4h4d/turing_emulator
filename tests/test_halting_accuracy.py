"""
Test suite for evaluating halting accuracy.
Verifies that the Turing Machine halts correctly for all operations.
"""
import unittest
from tm.simulator import TMSimulator
from tm.tape import Tape
from operations import build_initial_tape, get_generator_for
from config import MAX_STEPS


class TestHaltingAccuracy(unittest.TestCase):
    """Test halting behavior for all operations."""

    def test_halts_on_normal_completion(self):
        """Verify machine halts when operation completes normally."""
        tape = build_initial_tape(2, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        # Initially not halted
        self.assertFalse(sim.is_halted())
        
        # Run until completion
        while not sim.is_halted():
            trans = sim.step()
            if trans is None:
                break
        
        # Should be halted
        self.assertTrue(sim.is_halted())
        
        # Further steps should return None
        trans = sim.step()
        self.assertIsNone(trans)

    def test_halts_on_stop_iteration(self):
        """Verify machine halts when generator raises StopIteration."""
        tape = build_initial_tape(1, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        # Run until generator completes
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())

    def test_halts_on_max_steps(self):
        """Verify machine halts when max_steps is reached."""
        tape = build_initial_tape(1, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=5)  # Very low limit
        
        # Run until max steps
        while not sim.is_halted():
            trans = sim.step()
            if trans and trans[0] == 'HALT' and 'max steps' in str(trans[5]):
                break
        
        self.assertTrue(sim.is_halted())
        self.assertGreaterEqual(sim.step_count, 5)

    def test_halting_unary_add(self):
        """Test halting for unary addition."""
        tape = build_initial_tape(3, 2, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_halting_unary_subtract(self):
        """Test halting for unary subtraction."""
        tape = build_initial_tape(5, 2, 'unary')
        gen = get_generator_for('subtract', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_halting_unary_multiply(self):
        """Test halting for unary multiplication."""
        tape = build_initial_tape(2, 3, 'unary')
        gen = get_generator_for('multiply', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_halting_binary_add(self):
        """Test halting for binary addition."""
        tape = build_initial_tape(5, 3, 'binary')
        gen = get_generator_for('add', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_halting_binary_subtract(self):
        """Test halting for binary subtraction."""
        tape = build_initial_tape(7, 3, 'binary')
        gen = get_generator_for('subtract', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_halting_binary_multiply(self):
        """Test halting for binary multiplication."""
        tape = build_initial_tape(4, 3, 'binary')
        gen = get_generator_for('multiply', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertTrue(sim.is_halted())
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_halting_state_consistency(self):
        """Verify halting state remains consistent after halt."""
        tape = build_initial_tape(2, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        # Run until halt
        while not sim.is_halted():
            sim.step()
        
        # Verify multiple calls return same state
        self.assertTrue(sim.is_halted())
        self.assertTrue(sim.is_halted())
        self.assertTrue(sim.is_halted())
        
        # Verify step() returns None after halt
        self.assertIsNone(sim.step())
        self.assertIsNone(sim.step())


if __name__ == '__main__':
    unittest.main()

