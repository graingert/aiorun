import logging
import asyncio
from aiorun import run


logging.basicConfig(level='DEBUG')


async def main():
    await asyncio.sleep(5)


run(main())
logging.critical('Leaving fake main')