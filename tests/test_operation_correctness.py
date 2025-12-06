"""
Test suite for evaluating operation correctness.
Verifies that all arithmetic operations produce correct results.
"""
import unittest
from tm.simulator import TMSimulator
from tm.tape import Tape
from operations import build_initial_tape, get_generator_for
from config import MAX_STEPS, UNARY_SEP, BINARY_SEP, BLANK


class TestOperationCorrectness(unittest.TestCase):
    """Test correctness of all arithmetic operations."""

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

    # Unary Addition Tests
    def test_unary_add_small(self):
        """Test unary addition with small numbers."""
        result = self.run_operation(2, 1, 'add', 'unary')
        self.assertEqual(result, 3)

    def test_unary_add_zero(self):
        """Test unary addition with zero."""
        result = self.run_operation(0, 5, 'add', 'unary')
        self.assertEqual(result, 5)
        
        result = self.run_operation(5, 0, 'add', 'unary')
        self.assertEqual(result, 5)

    def test_unary_add_large(self):
        """Test unary addition with larger numbers."""
        result = self.run_operation(10, 5, 'add', 'unary')
        self.assertEqual(result, 15)

    # Unary Subtraction Tests
    def test_unary_subtract_normal(self):
        """Test unary subtraction with positive result."""
        result = self.run_operation(5, 2, 'subtract', 'unary')
        self.assertEqual(result, 3)

    def test_unary_subtract_zero_result(self):
        """Test unary subtraction resulting in zero."""
        result = self.run_operation(5, 5, 'subtract', 'unary')
        self.assertEqual(result, 0)

    def test_unary_subtract_clamp_to_zero(self):
        """Test unary subtraction clamping negative results to zero."""
        result = self.run_operation(2, 5, 'subtract', 'unary')
        self.assertEqual(result, 0)  # Should clamp to 0

    def test_unary_subtract_zero_operand(self):
        """Test unary subtraction with zero operand."""
        result = self.run_operation(5, 0, 'subtract', 'unary')
        self.assertEqual(result, 5)

    # Unary Multiplication Tests
    def test_unary_multiply_small(self):
        """Test unary multiplication with small numbers."""
        result = self.run_operation(2, 3, 'multiply', 'unary')
        self.assertEqual(result, 6)

    def test_unary_multiply_zero(self):
        """Test unary multiplication with zero."""
        result = self.run_operation(5, 0, 'multiply', 'unary')
        self.assertEqual(result, 0)
        
        result = self.run_operation(0, 5, 'multiply', 'unary')
        self.assertEqual(result, 0)

    def test_unary_multiply_one(self):
        """Test unary multiplication with one."""
        result = self.run_operation(5, 1, 'multiply', 'unary')
        self.assertEqual(result, 5)
        
        result = self.run_operation(1, 5, 'multiply', 'unary')
        self.assertEqual(result, 5)

    # Binary Addition Tests
    def test_binary_add_small(self):
        """Test binary addition with small numbers."""
        result = self.run_operation(3, 2, 'add', 'binary')
        self.assertEqual(result, 5)

    def test_binary_add_zero(self):
        """Test binary addition with zero."""
        result = self.run_operation(0, 5, 'add', 'binary')
        self.assertEqual(result, 5)
        
        result = self.run_operation(5, 0, 'add', 'binary')
        self.assertEqual(result, 5)

    def test_binary_add_with_carry(self):
        """Test binary addition with carry operations."""
        result = self.run_operation(5, 3, 'add', 'binary')
        self.assertEqual(result, 8)
        
        result = self.run_operation(7, 1, 'add', 'binary')
        self.assertEqual(result, 8)

    def test_binary_add_large(self):
        """Test binary addition with larger numbers."""
        result = self.run_operation(15, 7, 'add', 'binary')
        self.assertEqual(result, 22)

    # Binary Subtraction Tests
    def test_binary_subtract_normal(self):
        """Test binary subtraction with positive result."""
        result = self.run_operation(7, 3, 'subtract', 'binary')
        self.assertEqual(result, 4)

    def test_binary_subtract_zero_result(self):
        """Test binary subtraction resulting in zero."""
        result = self.run_operation(5, 5, 'subtract', 'binary')
        self.assertEqual(result, 0)

    def test_binary_subtract_clamp_to_zero(self):
        """Test binary subtraction clamping negative results to zero."""
        result = self.run_operation(3, 7, 'subtract', 'binary')
        self.assertEqual(result, 0)  # Should clamp to 0

    def test_binary_subtract_with_borrow(self):
        """Test binary subtraction with borrow operations."""
        result = self.run_operation(10, 3, 'subtract', 'binary')
        self.assertEqual(result, 7)

    # Binary Multiplication Tests
    def test_binary_multiply_small(self):
        """Test binary multiplication with small numbers."""
        result = self.run_operation(3, 2, 'multiply', 'binary')
        self.assertEqual(result, 6)

    def test_binary_multiply_zero(self):
        """Test binary multiplication with zero."""
        result = self.run_operation(5, 0, 'multiply', 'binary')
        self.assertEqual(result, 0)
        
        result = self.run_operation(0, 5, 'multiply', 'binary')
        self.assertEqual(result, 0)

    def test_binary_multiply_one(self):
        """Test binary multiplication with one."""
        result = self.run_operation(5, 1, 'multiply', 'binary')
        self.assertEqual(result, 5)
        
        result = self.run_operation(1, 5, 'multiply', 'binary')
        self.assertEqual(result, 5)

    def test_binary_multiply_large(self):
        """Test binary multiplication with larger numbers."""
        result = self.run_operation(7, 4, 'multiply', 'binary')
        self.assertEqual(result, 28)

    # Comprehensive Tests
    def test_all_operations_unary(self):
        """Test all operations with unary system."""
        # Addition
        self.assertEqual(self.run_operation(4, 3, 'add', 'unary'), 7)
        # Subtraction
        self.assertEqual(self.run_operation(4, 3, 'subtract', 'unary'), 1)
        # Multiplication
        self.assertEqual(self.run_operation(4, 3, 'multiply', 'unary'), 12)

    def test_all_operations_binary(self):
        """Test all operations with binary system."""
        # Addition
        self.assertEqual(self.run_operation(4, 3, 'add', 'binary'), 7)
        # Subtraction
        self.assertEqual(self.run_operation(4, 3, 'subtract', 'binary'), 1)
        # Multiplication
        self.assertEqual(self.run_operation(4, 3, 'multiply', 'binary'), 12)


if __name__ == '__main__':
    unittest.main()

