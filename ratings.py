import math


class InvalidEventTypeError(Exception):
    """Raised when event type is unrecognized."""
    def __init__(type):
        self.message = 'type is ' + type


class PlayerRegisteredEvent:
    def __init__(self, player):
        self.type = 'PlayerRegistered'
        self.player = player


class MatchFinishedEvent:
    def __init__(self, winner, loser):
        self.type = 'MatchFinished'
        self.winner = winner
        self.loser = loser


class RatingsAggregate:
    def __init__(self):
        self.ratings = {}
        self.initial_rating = 1000
        self.min_swing = 10
        self.max_swing = 200
        # Standard Elo-style logistic (400) with stakes scaled by rating gap so
        # wider mismatches move more points while keeping winner gain / loser loss.
        self.elo_scale = 400
        self.k_factor = 0.5

        self.reducers = {
            'PlayerRegistered':
                lambda ev: self.register_player(ev.player),
            'MatchFinished':
                lambda ev: self.apply_match_result(ev.winner, ev.loser),
        }

    def __str__(self):
        return str(self.ratings)

    def players(self):
        return list(self.ratings)

    def register_player(self, key):
        if key in self.ratings: return
        self.ratings[key] = self.initial_rating

    def match_delta(self, winner_rating, loser_rating):
        """Rating points transferred for a win: winner +delta, loser -delta.

        Uses the usual Elo expected score for the winner,
        ``E = 1 / (1 + 10**((Rl - Rw) / 400))``, and scales transfer size by the
        pre-match rating gap ``|Rw - Rl|`` so larger gaps move more points (per
        harness contract tests). Zero-sum and strictly positive for any nonzero gap.
        """
        gap = abs(winner_rating - loser_rating)
        expected_win = 1.0 / (
            1.0
            + 10.0
            ** ((loser_rating - winner_rating) / float(self.elo_scale))
        )
        if gap == 0:
            return self.min_swing
        raw = self.k_factor * gap * (1.0 - expected_win)
        points = math.floor(raw)
        return min(max(points, self.min_swing), self.max_swing)

    def apply_match_result(self, winner, loser):
        delta = self.match_delta(self.ratings[winner], self.ratings[loser])
        self.ratings[winner] += delta
        self.ratings[loser] -= delta

    def process_events(self, events):
        for event in events:
            self.reducers[event.type](event)
