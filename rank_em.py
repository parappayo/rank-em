import sys
import random
from ratings import MatchFinishedEvent, PlayerRegisteredEvent, RatingsAggregate


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
    events = []
    new_players = []
    with open(filename, 'r', encoding='utf-8') as infile:
        new_players = infile.readlines()
    for player in new_players:
        events.append(PlayerRegisteredEvent(player))
    return events

if __name__ == '__main__':
    ratings = RatingsAggregate()
    ratings.process_events(
        register_players_from_file(sys.argv[1]))
    ratings.process_events(
        prompt_round(ratings.players()))
    print(ratings)
