#! /usr/bin/env python3.8

from __future__ import annotations

import json
import asyncio
import functools

from typing import (
    Dict,
    List,
    Optional,
    Union,
    TypeVar,
    Iterable,
)

argumets = {
    'actor_file': 'actors.json',
    'data_file': 'tvdata.json',
    'target_file': 'relations.json'
}

Json = Union[List['Json'], Dict[str, Union['Json', int, str, type(None), bool]]]
_T = TypeVar('_T')

async def just_implement(movie: Json) -> Json:
    return {
        name: [
            rel_name
            for rel in movie['actors']
            if rel is not actor and (rel_name := rel.get('name', ''))
        ]
        for actor in movie['actors']
        if (name := actor.get('name', ''))
    }

def count(values: Iterable[_T], init: Optional[Dict[_T, int]] = None) -> Dict[_T, int]:
    if init is None:
        init = dict()
    for elem in values:
        init[elem] = init.get(elem, 0) + 1
    return init

def merge_and_clear(reduced: Json, _next: Json) -> Json:
    reduced.update({
        name: count(*values)
        for name in _next
        if (values := ((_next[name], reduced[name]) if name in reduced else (_next[name],)))
    })
    _next.clear()
    return reduced

def get_analysed(data: Json, loop: asyncio.AbstractEventLoop) -> Json:
    results = loop.run_until_complete(asyncio.gather(*map(just_implement, data.values())))
    return functools.reduce(merge_and_clear, results, dict())

def analyse(data_file: str, target_file: str, **kwargs) -> None:
    with open(data_file, 'r', encoding='utf-8') as file:
        data: Json = json.load(file)

    loop = asyncio.get_event_loop()
    analysed = get_analysed(data, loop)
    loop.close()
    with open(target_file, 'w', encoding='utf-8') as file:
        json.dump(analysed, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    analyse(**argumets)