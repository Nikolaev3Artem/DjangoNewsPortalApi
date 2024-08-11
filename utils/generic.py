from asgiref.sync import sync_to_async
from factory.django import DjangoModelFactory


class AsyncFactory(DjangoModelFactory):
    @classmethod
    async def acreate(cls, **kwargs):
        return await sync_to_async(cls.create)(**kwargs)

    @classmethod
    async def acreate_batch(cls, size, **kwargs):
        batch = []
        for _ in range(size):
            batch.append(await cls.acreate(**kwargs))
        return batch

    @classmethod
    async def abuild(cls, **kwargs):
        return await sync_to_async(cls.create)(**kwargs)

    @classmethod
    async def abuild_batch(cls, size, **kwargs):
        batch = []
        for _ in range(size):
            batch.append(await cls.abuild(**kwargs))
        return batch
