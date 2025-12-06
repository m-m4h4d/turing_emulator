"""
Test suite for evaluating transition count tracking.
Verifies that the simulator correctly counts transitions for each operation.
"""
import unittest
from tm.simulator import TMSimulator
from tm.tape import Tape
from operations import build_initial_tape, get_generator_for
from config import MAX_STEPS


class TestTransitionCount(unittest.TestCase):
    """Test transition count tracking for all operations."""

    def test_transition_count_tracks_steps(self):
        """Verify that step_count increments correctly."""
        tape = build_initial_tape(2, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        initial_count = sim.step_count
        self.assertEqual(initial_count, 0)
        
        # Execute a few steps
        for _ in range(5):
            sim.step()
        
        self.assertEqual(sim.step_count, 5)
        
        # Continue until halt
        while not sim.is_halted():
            sim.step()
        
        # Verify final count is reasonable (should be > 0)
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_unary_add_small(self):
        """Test transition count for small unary addition."""
        tape = build_initial_tape(1, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        # Small addition should complete in reasonable steps
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, 1000)

    def test_transition_count_unary_add_large(self):
        """Test transition count for larger unary addition."""
        tape = build_initial_tape(10, 5, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        # Larger addition should take more steps
        self.assertGreater(sim.step_count, 10)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_binary_add(self):
        """Test transition count for binary addition."""
        tape = build_initial_tape(5, 3, 'binary')
        gen = get_generator_for('add', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_unary_subtract(self):
        """Test transition count for unary subtraction."""
        tape = build_initial_tape(5, 2, 'unary')
        gen = get_generator_for('subtract', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_unary_multiply(self):
        """Test transition count for unary multiplication."""
        tape = build_initial_tape(3, 2, 'unary')
        gen = get_generator_for('multiply', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_binary_subtract(self):
        """Test transition count for binary subtraction."""
        tape = build_initial_tape(7, 3, 'binary')
        gen = get_generator_for('subtract', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_binary_multiply(self):
        """Test transition count for binary multiplication."""
        tape = build_initial_tape(4, 3, 'binary')
        gen = get_generator_for('multiply', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        self.assertGreater(sim.step_count, 0)
        self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_max_steps_limit(self):
        """Test that transition count respects max_steps limit."""
        tape = build_initial_tape(1, 1, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=10)  # Very low limit
        
        # Should halt at max_steps
        while not sim.is_halted():
            sim.step()
        
        # Should halt due to max steps
        self.assertGreaterEqual(sim.step_count, 10)
        self.assertTrue(sim.is_halted())


if __name__ == '__main__':
    unittest.main()

