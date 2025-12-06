"""
Test suite for edge cases.
Tests boundary conditions, zero values, and unusual inputs.
"""
import unittest
from tm.simulator import TMSimulator
from tm.tape import Tape
from operations import build_initial_tape, get_generator_for
from config import MAX_STEPS, INPUT_LIMIT


class TestEdgeCases(unittest.TestCase):
    """Test edge cases for all operations."""

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

    def run_operation(self, a: int, b: int, op: str, numeral: str) -> int:
        """Run operation and return result."""
        tape = build_initial_tape(a, b, numeral)
        gen = get_generator_for(op, numeral, tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        if numeral == 'unary':
            return self.extract_unary_result(sim.tape)
        else:
            return self.extract_binary_result(sim.tape)

    # Zero Tests
    def test_both_zeros_unary_add(self):
        """Test unary addition with both operands zero."""
        result = self.run_operation(0, 0, 'add', 'unary')
        self.assertEqual(result, 0)

    def test_both_zeros_binary_add(self):
        """Test binary addition with both operands zero."""
        result = self.run_operation(0, 0, 'add', 'binary')
        self.assertEqual(result, 0)

    def test_both_zeros_unary_subtract(self):
        """Test unary subtraction with both operands zero."""
        result = self.run_operation(0, 0, 'subtract', 'unary')
        self.assertEqual(result, 0)

    def test_both_zeros_binary_subtract(self):
        """Test binary subtraction with both operands zero."""
        result = self.run_operation(0, 0, 'subtract', 'binary')
        self.assertEqual(result, 0)

    def test_both_zeros_unary_multiply(self):
        """Test unary multiplication with both operands zero."""
        result = self.run_operation(0, 0, 'multiply', 'unary')
        self.assertEqual(result, 0)

    def test_both_zeros_binary_multiply(self):
        """Test binary multiplication with both operands zero."""
        result = self.run_operation(0, 0, 'multiply', 'binary')
        self.assertEqual(result, 0)

    # One Tests
    def test_one_operands_unary_add(self):
        """Test unary addition with one as operands."""
        result = self.run_operation(1, 1, 'add', 'unary')
        self.assertEqual(result, 2)

    def test_one_operands_binary_add(self):
        """Test binary addition with one as operands."""
        result = self.run_operation(1, 1, 'add', 'binary')
        self.assertEqual(result, 2)

    # Large Number Tests
    def test_large_numbers_unary_add(self):
        """Test unary addition with larger numbers."""
        result = self.run_operation(20, 15, 'add', 'unary')
        self.assertEqual(result, 35)

    def test_large_numbers_binary_add(self):
        """Test binary addition with larger numbers."""
        result = self.run_operation(20, 15, 'add', 'binary')
        self.assertEqual(result, 35)

    def test_large_numbers_unary_multiply(self):
        """Test unary multiplication with larger numbers."""
        result = self.run_operation(5, 4, 'multiply', 'unary')
        self.assertEqual(result, 20)

    def test_large_numbers_binary_multiply(self):
        """Test binary multiplication with larger numbers."""
        result = self.run_operation(5, 4, 'multiply', 'binary')
        self.assertEqual(result, 20)

    # Negative Clamping Tests
    def test_subtract_larger_from_smaller_unary(self):
        """Test unary subtraction when result would be negative."""
        result = self.run_operation(2, 5, 'subtract', 'unary')
        self.assertEqual(result, 0)  # Should clamp to 0

    def test_subtract_larger_from_smaller_binary(self):
        """Test binary subtraction when result would be negative."""
        result = self.run_operation(2, 5, 'subtract', 'binary')
        self.assertEqual(result, 0)  # Should clamp to 0

    # Halting Tests for Edge Cases
    def test_halts_on_zero_operands(self):
        """Verify machine halts correctly with zero operands."""
        for op in ['add', 'subtract', 'multiply']:
            for numeral in ['unary', 'binary']:
                tape = build_initial_tape(0, 0, numeral)
                gen = get_generator_for(op, numeral, tape)
                sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
                
                while not sim.is_halted():
                    sim.step()
                
                self.assertTrue(sim.is_halted())
                self.assertLess(sim.step_count, MAX_STEPS)

    def test_halts_on_single_one(self):
        """Verify machine halts correctly with single one operands."""
        for op in ['add', 'subtract', 'multiply']:
            for numeral in ['unary', 'binary']:
                tape = build_initial_tape(1, 1, numeral)
                gen = get_generator_for(op, numeral, tape)
                sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
                
                while not sim.is_halted():
                    sim.step()
                
                self.assertTrue(sim.is_halted())
                self.assertLess(sim.step_count, MAX_STEPS)

    # Transition Count Tests for Edge Cases
    def test_transition_count_zero_operands(self):
        """Test transition count with zero operands."""
        for op in ['add', 'subtract', 'multiply']:
            for numeral in ['unary', 'binary']:
                tape = build_initial_tape(0, 0, numeral)
                gen = get_generator_for(op, numeral, tape)
                sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
                
                while not sim.is_halted():
                    sim.step()
                
                # Should complete in reasonable steps
                self.assertGreater(sim.step_count, 0)
                self.assertLess(sim.step_count, MAX_STEPS)

    def test_transition_count_single_one(self):
        """Test transition count with single one operands."""
        for op in ['add', 'subtract', 'multiply']:
            for numeral in ['unary', 'binary']:
                tape = build_initial_tape(1, 1, numeral)
                gen = get_generator_for(op, numeral, tape)
                sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
                
                while not sim.is_halted():
                    sim.step()
                
                self.assertGreater(sim.step_count, 0)
                self.assertLess(sim.step_count, MAX_STEPS)

    # Input Validation Tests
    def test_input_validation_negative(self):
        """Test that negative inputs are rejected."""
        with self.assertRaises(ValueError):
            build_initial_tape(-1, 5, 'unary')
        
        with self.assertRaises(ValueError):
            build_initial_tape(5, -1, 'unary')

    def test_input_validation_large(self):
        """Test that inputs exceeding limit are rejected."""
        with self.assertRaises(ValueError):
            build_initial_tape(INPUT_LIMIT + 1, 5, 'unary')
        
        with self.assertRaises(ValueError):
            build_initial_tape(5, INPUT_LIMIT + 1, 'unary')

    # Result Format Tests
    def test_result_format_unary(self):
        """Test that unary results are in correct format."""
        tape = build_initial_tape(3, 2, 'unary')
        gen = get_generator_for('add', 'unary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        # Result should be all '1's (or blank for zero)
        content = sim.tape.as_str()
        valid_chars = set('1' + tape.blank)
        self.assertTrue(all(ch in valid_chars for ch in content))

    def test_result_format_binary(self):
        """Test that binary results are in correct format."""
        tape = build_initial_tape(5, 3, 'binary')
        gen = get_generator_for('add', 'binary', tape)
        sim = TMSimulator(tape, gen, max_steps=MAX_STEPS)
        
        while not sim.is_halted():
            sim.step()
        
        # Result should be valid binary (0s and 1s, or blank)
        content = sim.tape.as_str()
        valid_chars = set('01' + tape.blank)
        self.assertTrue(all(ch in valid_chars for ch in content))


if __name__ == '__main__':
    unittest.main()

