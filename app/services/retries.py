import asyncio
from typing import Callable, Awaitable


async def retry_async(
    func: Callable[[], Awaitable[None]],
    *,
    attempts: int = 3,
    delays: list[int] = [2, 6, 20],
):
    last_exc = None

    for i in range(attempts):
        try:
            await func()
            return
        except Exception as e:
            last_exc = e
            if i < attempts - 1:
                await asyncio.sleep(delays[i])

    raise last_exc
