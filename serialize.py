import json


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
