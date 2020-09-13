#! /usr/bin/env python3.8

import json

from typing import (
    Union,
    List,
    Dict,
)

Json = Union[List['Json'], Dict[str, Union['Json', int, str, type(None), bool]]]

arguments = {
    'file_name': 'relations.json',
    'target_name': 'top10.json',
}

def get_top10(data: Json) -> Json:
    return {
        name: {
            subname: subvalue
            for subname, subvalue in (name_list[:10] if len(name_list) > 10 else name_list)
        }
        for name, value in data.items()
        if (name_list := sorted(value.items(), key=lambda t: t[1], reverse=True))
    }

def write(file_name: str, target_name: str) -> None:
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    top10 = get_top10(data)
    with open(target_name, 'w', encoding='utf-8') as file:
        json.dump(top10, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    write(**arguments)