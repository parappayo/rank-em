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
        self.delta_factor = 0.8

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
        # TODO: this isn't working, the winner gets the same points whether they are
        # the higher or lower rated player
        delta = abs(winner_rating - loser_rating) * self.delta_factor
        distance = abs(self.initial_rating - (winner_rating + loser_rating) / 2)
        award = delta if loser_rating > winner_rating else self.max_swing - delta
        distance_div = max(distance / 100, 1)
        return min(max(math.floor(award / distance_div), self.min_swing), self.max_swing)

    def apply_match_result(self, winner, loser):
        delta = self.match_delta(self.ratings[winner], self.ratings[loser])
        self.ratings[winner] += delta
        self.ratings[loser] -= delta

    def process_events(self, events):
        for event in events:
            self.reducers[event.type](event)
