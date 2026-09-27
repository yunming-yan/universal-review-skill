import unittest

from calc import total_cents


class TestCalculator(unittest.TestCase):
    def test_positive_integers(self):
        self.assertEqual(total_cents(3, 125), 375)

    def test_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            total_cents(0, 125)


if __name__ == "__main__":
    unittest.main()
