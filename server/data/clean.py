#! /usr/bin/env python3.8

import json

from typing import (
    Union,
    List,
    Dict,
)

Json = Union[List['Json'], Dict[str, Union['Json', int, str, type(None), bool]]]

arguments = {
    'actors': 'actors.json',
    'relations': 'relations.json',
    'movies': 'tvdata.json',
}

def clean_object(actors: Json, relations: Json, movies: Json) -> Json:
    return {
        'actors' : actors,
        'relations': {
            name: {
                subname: count
                for subname, count in value.items()
                if subname in actors
            }
            for name, value in relations.items()
            if name in actors
        },
        'movies': {
            name: {
                subname: item if subname != 'actors' else [ actor for actor in item if actor['name'] in actors ]
                for subname, item in value.items()
            }
            for name, value in movies.items()
        }
    }


def clean(base: str, **kwargs) -> None:
    arg = {}
    for name, file_name in kwargs.items():
        with open(file_name, 'r', encoding='utf-8') as file:
            arg[name] = json.load(file)

    arg = clean_object(**arg)
    arg.pop(base)
    kwargs.pop(base)
    for name, file_name in kwargs.items():
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(arg[name], file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    clean('actors', **arguments)