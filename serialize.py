import json
from ratings import MatchFinishedEvent, PlayerRegisteredEvent, RatingsAggregate


def events_to_json(events):
    serializable = []
    for event in events:
        serializable.append(vars(event))
    return json.dumps(serializable)


def ratings_to_dict(ratings):
    return {
        'ratings': ratings.ratings,
        'initial_rating': ratings.initial_rating,
        'game_swing': ratings.game_swing,
        'delta_factor': ratings.delta_factor,
    }


def ratings_to_json(ratings):
    return json.dumps(ratings_to_dict(ratings))


def ratings_from_dict(ratings_dict):
    result = RatingsAggregate()
    result.ratings = ratings_dict['ratings']
    result.initial_rating = ratings_dict['initial_rating']
    result.game_swing = ratings_dict['game_swing']
    result.delta_factor = ratings_dict['delta_factor']
    return result


def ratings_from_json(json_str):
    return ratings_from_dict(json.loads(json_str))
