#! /usr/bin/env python3.8

import json
import sys
from typing import Iterable, Dict, Any

def merge(target_file: str, *source_list: Iterable[str]) -> None:
    with open(target_file, 'a+', encoding='utf-8') as file:
        try:
            json_obj: Dict[str, Any] = json.load(file)
        except:
            json_obj = dict()
    for source in source_list:
        with open(source, 'r', encoding='utf-8') as file:
            try:
                json_obj.update(json.load(file))
            except:
                print(f'{source} has some problem')

    with open(target_file, 'w', encoding='utf-8') as file:
        json.dump(json_obj, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    prefix = sys.argv[1]
    start, end = map(int, sys.argv[2].split(':'))
    merge(f"{prefix.strip(' _.')}.json", *(f'{prefix}{i}.json' for i in range(start, end)))
