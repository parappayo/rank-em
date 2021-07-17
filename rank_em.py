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

    events = []
    for player in new_players:
        events.append(PlayerRegisteredEvent(player))
    return events


if __name__ == '__main__':
    events = []
    ratings = RatingsAggregate()

    # TODO: read ratings from file

    # TODO: read events from file
    # new_events = read_events_from_file(events_filename)
    # events.extend(new_events)
    # ratings.process_events(new_events)

    new_events = register_players_from_file(players_filename)
    events.extend(new_events)
    ratings.process_events(new_events)

    new_events = prompt_round(ratings.players())
    events.extend(new_events)
    ratings.process_events(new_events)

    events_json = serialize.events_to_json(events)
    with open(events_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(events_json)

    # TODO: write ratings to file

    print(ratings)
