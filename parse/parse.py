import asyncio
from typing import Optional

import aiohttp

from config.parse_config import uuids


url_with_uuids = f'https://api.nike.com/cic/browse/v2?queryid=filteredProductsWithContext' \
      f'&uuids={",".join(uuids.values())}' \
      f'&language=ru' \
      f'&country=RU' \
      f'&channel=NIKE'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/95.0.4638.54 Safari/537.36"
}


async def parsing_data() -> Optional[list]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url_with_uuids, headers=headers) as response:
            all_data = await response.json()
            return all_data['data']['filteredProductsWithContext']['products']


def main():
    asyncio.run(parsing_data())


if __name__ == '__main__':
    main()
