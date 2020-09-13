#! /usr/bin/env python3.8

import aiohttp
import asyncio
import json
import sys
import logging

from typing import (
    Union,
    List,
    Dict,
    Any,
    Tuple,
    Optional,
)
from random import randrange
from bs4 import BeautifulSoup

from refine import refine_dict as refine

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger('scraper_data')
logger.addHandler(
    logging.FileHandler(filename="datalog.txt", mode='a+', encoding='utf-8')
)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4252.0 Safari/537.36",
}

Json = Dict[str, Union[Any, str, int, List['Json'], 'Json']]

class ConnectionFailed(Exception):
    pass

async def get(session: aiohttp.ClientSession, item: Json, item_num: int = 500, proxy: Optional[str] = None) -> Optional[BeautifulSoup]:
    url = item['url']
    await asyncio.sleep(randrange(0, 300) * 0.2)
    async with session.get(url, proxy=proxy) as resp:
        if 200 <= (stat := resp.status) < 400:
            logger.info(f"Successfully fetched {url}")
            return BeautifulSoup(await resp.text(), features='lxml')
        elif stat == 403:
            logger.error(f"Code 403 received")
        else:
            logger.error(f"Failed while fetching {url} with status code {stat}")
    raise ConnectionFailed(f'Code {stat}')


async def get_item(item: Json, item_num: int = 500) -> Tuple[BeautifulSoup, Json]:
    async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
        return await get(session, item, item_num), {name: item[name] for name in ['title', 'cover', 'url']}


def parse(html: BeautifulSoup, item: Json) -> Json:
    ret: Json = item
    ret['actors'] = [
        {
            'name': tag.text,
            'url': tag.attrs['href']
        }
        for tag in html.find_all('a', {'rel': 'v:starring'})
    ]
    try:
        summary = html.find_all('span', property='v:summary')[0].text
    except IndexError:
        summary = str()
    ret['summary'] = summary
    ret['comments'] = [comment.text for comment in html.find_all(
        'span', {'class': 'short'})]
    return ret


def full_data(data: List[Json], loop: asyncio.AbstractEventLoop) -> Dict[str, Json]:
    length = len(data)
    return {
        parsed['title']: parsed
        for retval in loop.run_until_complete(asyncio.gather(*(get_item(item, length) for item in data), return_exceptions=True))
        if retval is not None and not isinstance(retval, BaseException) and (parsed := parse(*retval))
    }


def fetch(target_list: List[Json], file_name: str) -> None:
    with open(file_name, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if not (data and isinstance(data, dict)):
                raise Exception()
        except Exception:
            data = dict()
    try:
        loop = asyncio.get_event_loop()
        data.update(
            full_data([
                item for item in target_list
                if item['title'] not in data
            ], loop)
        )
        refine(data)
    except Exception as e:
        logger.exception("Something wrong")
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        name_data = json.load(file)['subjects']
    fetch(name_data[1000:], sys.argv[2])
