import asyncio
import logging
import platform

import aiohttp

from config import headers, url_with_uuids

log = logging.getLogger(__name__)


async def parse_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url_with_uuids, headers=headers) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.json()


if __name__ == "__main__":
    if platform.system() == 'Windows':  # On Windows seems to be a problem with EventLoopPolicy
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(parse_data())