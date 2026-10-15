import unittest

from src.algorithms import first_unique_index


class TestFirstUniqueIndex(unittest.TestCase):
    def test_case_sensitive_characters(self):
        self.assertEqual(first_unique_index("aA"), 0)

    def test_first_unique_character(self):
        self.assertEqual(first_unique_index("aab"), 2)

    def test_no_unique_character(self):
        self.assertEqual(first_unique_index("aabb"), -1)

    def test_empty_string(self):
        self.assertEqual(first_unique_index(""), -1)


if __name__ == "__main__":
    unittest.main()