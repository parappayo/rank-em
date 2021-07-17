import sys
import random


# https://en.wikipedia.org/wiki/Elo_rating_system
def new_elo_ratings(winner_rating, loser_rating):
    return (loser_rating + 400, winner_rating - 400)


def init_elo_ratings(items):
    ratings = {}
    for item in items:
        ratings[item] = 1200
    return ratings    


def adjust_elo_ratings(ratings, winner, loser):
    new_ratings = new_elo_ratings(ratings[winner], ratings[loser])
    ratings[winner] = new_ratings[0]
    ratings[loser] = new_ratings[1]


def prompt_faceoff(itemA, itemB):
    print('a:', itemA, 'b:', itemB)
    choice = False
    while choice != 'a' and choice != 'b':
        choice = input()
    return choice


def prompt_elo_round(ratings):
    items = list(ratings)
    random.shuffle(items)
    for i in range(0, len(items)-1, 2):
        itemA, itemB = items[i], items[i+1]
        choice = prompt_faceoff(itemA, itemB)
        if choice == 'a':
            adjust_elo_ratings(ratings, itemA, itemB)
        elif choice == 'b':
            adjust_elo_ratings(ratings, itemB, itemA)


def prompt_rankings(items):
    ratings = init_elo_ratings(items)
    prompt_elo_round(ratings)
    return ratings


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as infile:
        result = prompt_rankings(infile.readlines())
    print(result)
