import unittest
from src.cleaner import normalize_brackets

class TestCleaner(unittest.TestCase):

    def test_normalize_brackets(self):
        # Checks that restoration brackets are removed and whitespace cleaned from text.
        self.assertEqual(normalize_brackets("[LÚ]NAR"), "LÚNAR")
        self.assertEqual(normalize_brackets("  [É]   GAL  "), "É GAL")
        
    def test_normalize_editorial_marks(self):
        # Checks that correction (!) and uncertainty (?) marks are removed from text.
        self.assertEqual(normalize_brackets("LÚ?"), "LÚ")
        self.assertEqual(normalize_brackets("[É!] GAL?"), "É GAL")

if __name__ == '__main__':
    unittest.main()