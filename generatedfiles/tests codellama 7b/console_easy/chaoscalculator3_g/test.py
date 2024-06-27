
import unittest
import BasicMathOperation

class TestBasicMathOperation(unittest.TestCase):

    def test_get_inputs(self):
        basic_math_operation = BasicMathOperation()
        num1, num2 = basic_math_operation.get_inputs()
        self.assertIsInstance(num1, int)
        self.assertIsInstance(num2, int)
        self.assertGreaterEqual(num1, 0)
        self.assertGreaterEqual(num2, 0)

    def test_apply_operation(self):
        basic_math_operation = BasicMathOperation()
        operation = basic_math_operation.apply_operation(10, 5)
        self.assertEqual(operation, 15)

    def test_ask_operation(self):
        basic_math_operation = BasicMathOperation()
        operation = basic_math_operation.ask_operation(10, 5)
        self.assertIn(operation, ("addition", "subtraction", "multiplication", "division"))

    def test_check_result(self):
        basic_math_operation = BasicMathOperation()
        result = basic_math_operation.check_result(10, 5, "addition")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
