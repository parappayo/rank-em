# rank-em

Quick n dirty tools for ranking things

Implemented in [Python 3](https://www.python.org/).

## Getting Started

This project is not yet in a working state.

## Goals

* Input through [cli prompts](https://docs.python.org/3/library/functions.html#input)
* Persistence as local [json file](https://docs.python.org/3/library/json.html)
* [Elo style](https://en.wikipedia.org/wiki/Elo_rating_system) rating system
* [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) architecture
* [Unit Tests](https://docs.python.org/3/library/unittest.html)

## Terminology

* Match - a contest between two players resulting in one player being the winner and the other being the loser
* Player - a registered contestant identified by a string key, could be any entity
* Ratings - aggregate of player ratings obtained by applying match results

## Future Considerations

* Configurable persistence as [Postgres](https://www.postgresql.org/), [Mongo](https://www.mongodb.com/), [Redis](https://redis.io/), or [Sqlite](https://www.sqlite.org/)
* [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) via [Flask](https://flask.palletsprojects.com/)
* [GraphQL](https://graphql.org/)
* [Web-Queue-Worker Architecture](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/web-queue-worker)
* Infrastructure as [Docker](https://www.docker.com/), [AWS Lambda](https://aws.amazon.com/lambda/), or [Heroku](https://www.heroku.com/)
