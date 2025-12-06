"""
Test runner script to execute all test suites.
Provides a comprehensive evaluation of transition count and halting accuracy.
"""
import unittest
import sys
from io import StringIO

# Import all test modules
from tests.test_transition_count import TestTransitionCount
from tests.test_halting_accuracy import TestHaltingAccuracy
from tests.test_operation_correctness import TestOperationCorrectness
from tests.test_edge_cases import TestEdgeCases
from tests.test_integration import TestIntegration


def run_all_tests(verbose=True):
    """Run all test suites and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTransitionCount))
    suite.addTests(loader.loadTestsFromTestCase(TestHaltingAccuracy))
    suite.addTests(loader.loadTestsFromTestCase(TestOperationCorrectness))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    stream = StringIO() if not verbose else sys.stderr
    runner = unittest.TextTestRunner(stream=stream, verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    return result


def print_summary(result):
    """Print a summary of test results."""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    print("="*70)


if __name__ == '__main__':
    print("Running comprehensive test suite for Turing Machine Emulator...")
    print("Testing: Transition Count, Halting Accuracy, Operation Correctness, Edge Cases, Integration")
    print()
    
    result = run_all_tests(verbose=True)
    print_summary(result)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)

