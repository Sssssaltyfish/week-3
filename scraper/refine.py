#! /usr/bin/env python3.8

import json
import sys

from typing import (
    Dict,
    Iterable,
    List
)

def refined(string: str) -> str:
    return '\n'.join([stripped for subcomment in string.strip().splitlines() if (stripped := subcomment.strip())])

def refine_dict(data: Dict[str, Dict[str, str]], item_name: str = 'summary') -> None:
    waiting_to_pop: List[str] = list()
    for name, item in data.items(): 
        if item.get('comments', []) or item.get('summary', '') or item.get('actors', []):
            item.update({ item_name: refined(item[item_name]) })
        else:
            print(item.get('title', ''))
            waiting_to_pop.append(name)
    for name in waiting_to_pop:
        data.pop(name)
    print(len(data))


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as read:
        data: Iterable[Dict[str, str]] = json.load(read)
    refine_dict(data)
    with open(sys.argv[2], 'w', encoding='utf-8') as write:
        json.dump(data, write, ensure_ascii=False, indent=4)
