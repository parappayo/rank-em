import os
import random
import serialize
import sys
from ratings import MatchFinishedEvent, PlayerRegisteredEvent, RatingsAggregate


players_filename = 'players.txt'
events_filename = 'events.json'
ratings_filename = 'ratings.json'


class InvalidChoiceError(Exception):
    """Raised when prompt result is unrecognized."""
    def __init__(choice):
        self.message = 'choice is ' + choice


def create_match_finished_event(choice, playerA, playerB):
    if choice == 'a':
        return MatchFinishedEvent(playerA, playerB)
    elif choice == 'b':
        return MatchFinishedEvent(playerB, playerA)
    raise InvalidChoiceError(choice)


def prompt_match(playerA, playerB):
    print('a:', playerA, 'b:', playerB)
    choice = False
    while choice != 'a' and choice != 'b':
        choice = input()
    return choice


def prompt_round(players):
    events = []
    random.shuffle(players)
    for i in range(0, len(players)-1, 2):
        playerA, playerB = players[i], players[i+1]
        choice = prompt_match(playerA, playerB)
        events.append(
            create_match_finished_event(choice, playerA, playerB))
    return events


def register_players_from_file(filename):
    new_players = []
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            new_players = infile.readlines()
    except FileNotFoundError:
        return []

    return list(map(lambda p: PlayerRegisteredEvent(p), new_players))


def read_ratings_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        return serialize.ratings_from_json(infile.read())


def read_events_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        return serialize.events_from_json(infile.read())


def serialize_to_file(filename, data, serialize_func):
    json_str = serialize_func(data)
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(json_str)


if __name__ == '__main__':
    events = []
    ratings = RatingsAggregate()

    if os.path.isfile(ratings_filename):
        ratings = read_ratings_from_file(ratings_filename)
    else:
        new_events = read_events_from_file(events_filename)
        events.extend(new_events)
        ratings.process_events(new_events)

    new_events = register_players_from_file(players_filename)
    events.extend(new_events)
    ratings.process_events(new_events)

    new_events = prompt_round(ratings.players())
    events.extend(new_events)
    ratings.process_events(new_events)

    serialize_to_file(events_filename, events, serialize.events_to_json)
    serialize_to_file(ratings_filename, ratings, serialize.ratings_to_json)

    print(ratings)
