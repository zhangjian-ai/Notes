import aioredis
import asyncio
import traceback
import logging

logging.basicConfig(level='INFO')
logger = logging.getLogger('redis')


class Redis:
    _redis = None

    def __init__(self):
        self._redis = aioredis.Connection(host='121.4.47.229', port=6379, db=5)

    async def get_conn(self):
        try:
            await self._redis.connect()
        except:
            logger.error('redis connect is failure ... \n', traceback.format_exc())

    async def execute(self, command):
        await self._redis.send_command(command)

    async def close(self):
        if self._redis:
            await self._redis.disconnect()


if __name__ == '__main__':
    redis = Redis()
    loop = asyncio.get_event_loop()

    loop.run_until_complete(redis.get_conn())
    loop.run_until_complete(redis.execute('sadd mobile 1340026934'))
    loop.run_until_complete(redis.close())

    # name = loop.run_until_complete(asyncio.wait(conn.pack_command('GET', 'name')))

