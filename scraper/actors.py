#! /usr/bin/env python3.8

import multiprocessing
import sys
import os
import json
import logging
import asyncio
from tkinter import EXCEPTION
import aiohttp

from bs4 import BeautifulSoup, Tag
from typing import Iterable, Tuple
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

import data

from data import Json, headers
from refine import refined

logger = logging.getLogger('scraper_actor')
logger.addHandler(
    logging.FileHandler(filename="actorlog.txt", mode='a+', encoding='utf-8')
)

class URLException(Exception):
    pass

async def get_item(session: aiohttp.ClientSession, item: Json, item_num: int = 500, **kwargs) -> Tuple[BeautifulSoup, Json]:
    url = item['url']
    if url.startswith('/'):
        item['url'] = f'https://movie.douban.com{url}'
    if not url.startswith('/celebrity'):
        if url.startswith('/subject_search?'):
            #item['url'] = (await data.get(item, 1)).find('a', {'class': 'title-text'}).attrs['href']
            raise URLException(f"Unusual url {url}")
        else:
            logger.warning(f"Unknown actor url {url}")
    return await data.get(session, item, item_num, **kwargs), { name: item[name] for name in ['name', 'url'] }


def parse(html: BeautifulSoup, item: Json) -> Json:
    ret: Json = item
    try:
        summary = html.find_all('span', {'class': 'all hidden'})[0].text
    except IndexError:
        try:
            summary = html.find('div', {'id': 'intro', 'class': 'mod'}).find('div', {'class': 'bd'}).text
        except Exception:
            summary = str()
    ret['summary'] = refined(summary)
    ret['cover'] = html.find('img')['src']
    html = html.find('div', {'class': 'info'}).find('ul')
    informations = html.children
    ret['info'] = {
        splitted[0]: splitted[1]
        for tag in informations
        if isinstance(tag, Tag) and (splitted := [
            text
            for unstripped in tag.text.splitlines()
            if (text := unstripped.strip(' ：:'))
        ])
    }
    logger.info(f"New data {item['name']}")
    return ret

def write(item_list: Iterable[Json], file_name: str, **kwargs):
    length = len(item_list)
    with open(file_name, 'a+', encoding='utf-8'):
        pass
    with open(file_name, 'r', encoding='utf-8') as file:
        try:
            data: Json = json.load(file)
        except Exception:
            data = dict()
    async def a():
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
        #async with aiohttp.ClientSession(headers=headers) as session:
            async def write_single(item: Json):
                try:
                    item = parse(*(await get_item(session, item, length, **kwargs)))
                    data.update({ item['name']: item })
                except Exception as e:
                    if not isinstance(e, URLException):
                        logger.exception("Exception occurred")
                else:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

            await asyncio.gather(*map(write_single, item_list), return_exceptions=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(a())
    loop.close()


if __name__ == '__main__':
    #source, target = sys.argv[1], sys.argv[2]
    source, target = 'actors_name.json', 'actors.json'
    with open(source, 'r') as source_file:
        actors: Json = json.load(source_file)
    with open(target, 'r') as check_file:
        check = json.load(check_file)
        item_list = [
            value
            for name, value in actors.items()
            if name not in check
        ]
        del check

    number = 40
    length = len(item_list)
    span = length//number
    processes = [
        Process(target=write, args=(item_list[i*span:(i+1)*span], f'actors/actors_{i}.json'), daemon=True)
        for i in range(number)
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
