import unittest

from ratings import RatingsAggregate


class TestRankingAlgorithmRequirements(unittest.TestCase):
    """Contract tests for any tournament rating update: post-match incentives and monotonicity."""

    def test_winner_rating_increases_after_match(self):
        scenarios = [
            # winner_key, loser_key, winner_rating_before, loser_rating_before
            ("w", "l", 1000, 1000),
            ("w", "l", 900, 1100),
            ("w", "l", 1200, 800),
            ("ala", "bob", 1050, 1040),
        ]
        for winner, loser, rw, rl in scenarios:
            with self.subTest(winner=winner, loser=loser, rw=rw, rl=rl):
                agg = RatingsAggregate()
                agg.register_player(winner)
                agg.register_player(loser)
                agg.ratings[winner] = rw
                agg.ratings[loser] = rl
                before_w = agg.ratings[winner]
                agg.apply_match_result(winner, loser)
                self.assertGreater(
                    agg.ratings[winner],
                    before_w,
                    "Winner's rating should strictly increase after a win.",
                )

    def test_loser_rating_decreases_after_match(self):
        scenarios = [
            ("w", "l", 1000, 1000),
            ("w", "l", 900, 1100),
            ("w", "l", 1200, 800),
            ("ala", "bob", 1050, 1040),
        ]
        for winner, loser, rw, rl in scenarios:
            with self.subTest(winner=winner, loser=loser, rw=rw, rl=rl):
                agg = RatingsAggregate()
                agg.register_player(winner)
                agg.register_player(loser)
                agg.ratings[winner] = rw
                agg.ratings[loser] = rl
                before_l = agg.ratings[loser]
                agg.apply_match_result(winner, loser)
                self.assertLess(
                    agg.ratings[loser],
                    before_l,
                    "Loser's rating should strictly decrease after a loss.",
                )

    def test_winner_point_gain_increases_with_larger_pre_match_rating_gap(self):
        """Larger |winner − loser| before the match ⇒ larger winner delta (points gained).

        Covers both cases: upset (winner starts lower) and favorite (winner starts higher).
        """
        agg = RatingsAggregate()

        upset_cases = [
            # (gap, winner_rating, loser_rating) — winner is lower-rated; gap widens
            (40, 980, 1020),
            (100, 950, 1050),
            (200, 900, 1100),
        ]
        for i in range(len(upset_cases) - 1):
            g1, w1, l1 = upset_cases[i]
            g2, w2, l2 = upset_cases[i + 1]
            with self.subTest(branch="upset", gap_lo=g1, gap_hi=g2):
                self.assertLess(g1, g2)
                d1 = agg.match_delta(w1, l1)
                d2 = agg.match_delta(w2, l2)
                self.assertLess(
                    d1,
                    d2,
                    "When the winner was lower-rated, a wider pre-match rating gap "
                    "should award the winner strictly more points.",
                )

        favorite_cases = [
            # (gap, winner_rating, loser_rating) — winner is higher-rated; gap widens
            (40, 1020, 980),
            (100, 1050, 950),
            (200, 1100, 900),
        ]
        for i in range(len(favorite_cases) - 1):
            g1, w1, l1 = favorite_cases[i]
            g2, w2, l2 = favorite_cases[i + 1]
            with self.subTest(branch="favorite", gap_lo=g1, gap_hi=g2):
                self.assertLess(g1, g2)
                d1 = agg.match_delta(w1, l1)
                d2 = agg.match_delta(w2, l2)
                self.assertLess(
                    d1,
                    d2,
                    "When the winner was higher-rated, a wider pre-match rating gap "
                    "should still award the winner strictly more points.",
                )


class TestRatingsMethods(unittest.TestCase):
    def test_match_delta(self):
        tests = [
            # (winner rating, loser rating, expected)
            (1000, 1000, 200),
            (950, 1050, 80),
            (900, 1100, 160),
            (850, 1150, 200),
            (800, 1200, 200),
            (1100, 1300, 80),
            (1200, 1400, 53),
            (1300, 1500, 40),
            (1400, 1600, 32),
            (900, 700, 20),
        ]
        agg = RatingsAggregate()
        for test in tests:
            winner_rating, loser_rating, expected = test
            result = agg.match_delta(winner_rating, loser_rating)
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
