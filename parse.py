import asyncio
from typing import Optional

import aiohttp

from config import headers, url_with_uuids


async def parsing_data() -> Optional[list]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url_with_uuids, headers=headers) as response:
            all_data = await response.json()
            return all_data["data"]["filteredProductsWithContext"]["products"]


def main():
    asyncio.run(parsing_data())


if __name__ == "__main__":
    main()
