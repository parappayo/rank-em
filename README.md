# rank-em

Quick n dirty tools for ranking things

Implemented in [Python 3](https://www.python.org/).

## Getting Started

* Populate `players.txt` with new players to be registered
  * Any already registered players in `ratings.json` are ignored
* Run `python3 rank_em.py` for a series of cli prompts to record round of matches
* Event history is persisted to `events.json`
  * If `ratings.json` is not present on start, this file is used to create a new aggregate
* New ratings are persisted to `ratings.json`
  * This will be used as a snapshot for the next invocation

## Goals

* Input through [cli prompts](https://docs.python.org/3/library/functions.html#input)
* Persistence as local [json file](https://docs.python.org/3/library/json.html)
* [Elo style](https://en.wikipedia.org/wiki/Elo_rating_system) rating system
* [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) architecture
* [Unit Tests](https://docs.python.org/3/library/unittest.html)

### TODO

* Print human-readable ranking at the end
* Fix rating adjustment formula
  * Points transfered is proportional to player delta when the winner is the lower rated player
  * Points transfered is inversely proportional to player delta when the winner is the higher rated player
  * Points transfered is inversely proportional to the distance from staring value
* Ladder matches instead of shuffle
* Event envelope
  * Type, version, event time, payload
  * SQL table schema sketched out
* Fix: do not generate redundant register player events
* Instructions to remove a game result from history and regenerate ratings

## Terminology

* Aggregate - state derived from reducing a series events
* Event - record of something having happend
* Ladder - when players are matched based on their ranking neighbours
* Match - a contest between two players resulting in one player being the winner and the other being the loser
* Player - a registered contestant identified by a string key, could be any entity
* Ranking - a player's standing in the list of registered players
* Rating - aggregate measure of player performance obtained by applying match results
* Reducer - function that updates state based on an event

## Future Considerations

* [orjson](https://github.com/ijl/orjson) or [Pickle](https://docs.python.org/3/library/pickle.html) for better [JSON](https://www.json.org/) serialization
* Configurable persistence as [Postgres](https://www.postgresql.org/), [Mongo](https://www.mongodb.com/), [Redis](https://redis.io/), or [Sqlite](https://www.sqlite.org/)
* [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) via [Flask](https://flask.palletsprojects.com/)
* [GraphQL](https://graphql.org/)
* [Web-Queue-Worker Architecture](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/web-queue-worker)
* Infrastructure as [Docker](https://www.docker.com/), [AWS Lambda](https://aws.amazon.com/lambda/), or [Heroku](https://www.heroku.com/)
