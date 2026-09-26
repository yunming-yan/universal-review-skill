import unittest
from converter import convert


class ExistingTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(convert([]), [])

    def test_utc(self):
        self.assertEqual(
            convert([{"id": "one", "timestamp": "2026-01-01T00:00:00+00:00", "quantity": 3}]),
            [{"id": "one", "timestamp": "2026-01-01T00:00:00Z", "quantity": 3}],
        )


if __name__ == "__main__":
    unittest.main()
