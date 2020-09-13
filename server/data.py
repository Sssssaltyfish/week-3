#! /usr/bin/env python3.8

import logging
import json

from typing import Dict, List, Union
try:
    from search.models import *
    from server.search.models import *
except:
    pass

data = {
    'actors': 'data/actors.json',
    'relations': 'data/top10.json',
    'movies': 'data/tvdata.json',
}

Json = Union[List['Json'], Dict[str, Union['Json', int, str, type(None), bool]]]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="datalog.txt",
    filemode='a+',
)
logger = logging.getLogger('data')

def write(actors_data: Json, relations_data: Json, movies_data: Json) -> None:
    try:
        actors: Dict[str, Actor] = {
            name: ret[0]
            for name, value in actors_data.items()
            if (
                (ret := Actor.objects.get_or_create(**value))
                and (
                    logger.info(f'Actor {name} ' + ('added' if ret[1] else 'found'))
                    or True
                )
            )
        }
    except Exception:
        logger.exception(f'Exception occurred: Actors')

    for name, value in actors.items():
        try:
            for related_name, count in relations_data[name].items():
                value.relations.add(actors[related_name], through_defaults={ 'count': count })
        except Exception:
            logger.exception(f'Exception occurred: related actor {name}-{related_name}')
        else:
            value.save(force_update=True)

    for name, value in movies_data.items():
        related_actors = value.pop('actors', [])
        url = value.pop('url', '')
        if url:
            logger.info(f'Movie {name}: {url}')
        try:
            movie, created = Movie.objects.get_or_create(**value)
        except Exception:
            logger.exception(f'Exception occurred: Movie {name}')
        for actor_name in map(lambda actor: actor.get('name', ''), related_actors):
            try:
                movie.actors.add(actors[actor_name])
            except Exception:
                logger.exception(f'Exception occurred: Movie {name} actor {actor_name}')
        logger.info(f'Movie {name} added')

def from_files(**kwargs) -> None:
    arguments = {}
    for argname, file_name in kwargs.items():
        with open(file_name, 'r', encoding='utf-8') as file:
            arguments[f'{argname}_data'] = json.load(file)
    write(**arguments)

def main():
    from_files(**data)

if __name__ == "__main__":
    main()