import unittest
from src.cleaner import normalize_brackets

class TestCleaner(unittest.TestCase):

    def test_normalize_brackets_removes_square_brackets(self):
        sample_input = "[LÚ]NAR"
        expected_output = "LÚNAR"
        self.assertEqual(normalize_brackets(sample_input), expected_output)

    def test_normalize_brackets_handles_whitespace(self):
        sample_input = "  [É]   GAL  "
        expected_output = "É GAL"
        self.assertEqual(normalize_brackets(sample_input), expected_output)

if __name__ == '__main__':
    unittest.main()