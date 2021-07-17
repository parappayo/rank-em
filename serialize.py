import json


class InvalidEventError(Exception):
    """Raised when an event type is unrecognized."""
    def __init__(event_type):
        self.message = 'event_type is ' + event_type


def event_to_dict(event):
    if event.type == 'PlayerRegistered':
        return {
            'type': 'PlayerRegistered',
            'player': event.player
        }
    elif event.type == 'MatchFinished':
        return {
            'type': 'MatchFinished',
            'winner': event.winner,
            'loser': event.loser,
        }
    raise InvalidEventError(event.type)


def events_to_json(events):
    serializable = []
    for event in events:
        serializable.append(event_to_dict(event))
    return json.dumps(serializable)
