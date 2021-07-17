import sys
import random


# https://en.wikipedia.org/wiki/Elo_rating_system
def elo_point_delta(winner_rating, loser_rating):
    return (loser_rating + 400, winner_rating - 400)


def init_ratings(items):
    ratings = {}
    for item in items:
        ratings[item] = 1200
    return ratings    


def prompt_faceoff(item1, item2):
    print('A:', item1, 'B:', item2)
    choice = input()


def prompt_round(ratings):
    items = list(ratings)
    random.shuffle(items)
    for i in range(0, len(items)-1, 2):
        prompt_faceoff(items[i], items[i+1])


def prompt_rankings(items):
    ratings = init_ratings(items)
    prompt_round(ratings)


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as infile:
        result = prompt_rankings(infile.readlines())
    print(result)
