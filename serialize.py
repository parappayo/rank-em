import json
from ratings import InvalidEventTypeError, MatchFinishedEvent, PlayerRegisteredEvent, RatingsAggregate


def events_to_json(events):
    serializable = []
    for event in events:
        serializable.append(vars(event))
    return json.dumps(serializable)


def event_from_dict(event_dict):
    if event_dict['type'] == 'PlayerRegistered':
        return PlayerRegisteredEvent(event_dict['player'])
    elif event_dict['type'] == 'MatchFinished':
        return MatchFinishedEvent(event_dict['winner'], event_dict['loser'])
    raise InvalidEventTypeError(event_dict.type)


def events_from_json(json_str):
    events = json.loads(json_str)
    return list(map(lambda e: event_from_dict(e), events))


def ratings_to_dict(ratings):
    return {
        'ratings': ratings.ratings,
        'initial_rating': ratings.initial_rating,
        'min_swing': ratings.min_swing,
        'max_swing': ratings.max_swing,
        'k_factor': ratings.k_factor,
        'elo_scale': ratings.elo_scale,
    }


def ratings_to_json(ratings):
    return json.dumps(ratings_to_dict(ratings))


def ratings_from_dict(ratings_dict):
    result = RatingsAggregate()
    result.ratings = ratings_dict['ratings']
    result.initial_rating = ratings_dict['initial_rating']
    result.min_swing = ratings_dict['min_swing']
    result.max_swing = ratings_dict['max_swing']
    result.k_factor = ratings_dict.get('k_factor', 0.5)
    result.elo_scale = ratings_dict.get('elo_scale', 400)
    return result


def ratings_from_json(json_str):
    return ratings_from_dict(json.loads(json_str))
