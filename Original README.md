# SPRK Coding Challenge
Dear Mikael, thanks for taking the time to complete our coding challenge. Instead of repeating the same boring challenges over and over again, we thought we would rather do something more practical and closer to the actual day-to-day work at SPRK.

## The Scenario
Let's assume that one of our pickers is scanning a multitude of products with our mobile app and submits the session to our Backend service. Unfortunately we can't control the version he uses to do this (for whatever reason). So the data we receive may be corrupted.
1. Products are identified using the field `code` in combination with the field `type`
2. The `code` field should not contain any leading zeros once it is stored in our database.
3. The `code` may be a mix of both, ones with leading zeros and without them.
4. There may be unicode characters which need to be parsed before storing in our database.
5. The field `trade_item_unit_descriptor` may also be present as `trade_item_descriptor` but should be transformed to the first before being stored in the DB. 

## Your Task
Your task is to build an API in python which can:
1. receive the [product feed](products.json), normalize it, and store it in a PostgreSQL database.
2. return the stored product info individually (by code) or the entire range as an array if no argument is passed.

## Requirements
1. The application should be built in a way so that it is runnable via dockerization and can be launched with a single [docker-compose](https://docs.docker.com/compose/) command.
2. The products need to be deduplicated (removing leading zeros from the code and merging the amounts).

## Hints
Refer to the [docker docs](https://docs.docker.com/language/python/) for support.
