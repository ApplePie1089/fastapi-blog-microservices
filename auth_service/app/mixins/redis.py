import asyncio

from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError
from app.configs import redis_settings
from app.meta.singleton import Singleton

from typing import Callable


class SingleRedisSession(metaclass=Singleton):

    def __init__(self):
        retry = None
        retry_on_error = None
        if redis_settings.REDIS_RETRY:
            retry = Retry(
                ExponentialBackoff(),
                redis_settings.REDIS_RETRY_COUNT,
            )
            retry_on_error = [ConnectionError]

        self._redis = Redis(
            host=redis_settings.REDIS_HOST,
            password=redis_settings.REDIS_PASSWORD,
            port=redis_settings.REDIS_PORT,
            decode_responses=True,
            retry=retry,
            retry_on_error=retry_on_error
        )

    def get_session(self) -> Redis:
        return self._redis


class RedisMixin:
    def __init__(self):
        super().__init__()
        self._redis = SingleRedisSession().get_session()

    async def start_consuming(self, channel: str, callback: Callable, prefetch_count: int = 5):
        async with self._redis.pubsub() as pubsub:
            pubsub: PubSub
            await pubsub.subscribe(channel)
            task = asyncio.create_task(
                self._consume(
                    channel=pubsub,
                    callback=callback,
                    prefetch_count=prefetch_count
                ),
                name=f"Consume from {channel}"
            )
            await task

    @staticmethod
    async def _consume(channel: PubSub, callback: Callable, prefetch_count: int = 5):
        batch = []
        async for message in channel.get_message():
            if message:
                batch.append(callback(message))
                if len(batch) >= prefetch_count:
                    await asyncio.gather(*batch)
                    batch = []
            else:
                if batch:
                    await asyncio.gather(*batch)
                    batch = []
                else:
                    await asyncio.sleep(0.1)

    async def publish_to_channel(self, channel_name: str, message: str):
        await self._redis.publish(channel=channel_name, message=message)