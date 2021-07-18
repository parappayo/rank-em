import unittest
from ratings import RatingsAggregate


class TestRatingsMethods(unittest.TestCase):
    def test_match_delta(self):
        tests = [
            # (winner rating, loser rating, expected)
            (1000, 1000, 10),
            (950, 1050, 80),
            (900, 1100, 160),
            (850, 1150, 200),
            (800, 1200, 200),
            (1100, 1300, 80),
            (1200, 1400, 53),
            (1300, 1500, 40),
            (1400, 1600, 32),
            (900, 700, 80),
        ]
        agg = RatingsAggregate()
        for test in tests:
            winner_rating, loser_rating, expected = test
            result = agg.match_delta(winner_rating, loser_rating)
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
