from __future__ import annotations

import time
from typing import Optional

try:
    from redis.asyncio import Redis
except Exception:
    Redis = None




LOCK_PREFIX = "wfo:lock:"
IDEMPOTENCY_PREFIX = "wfo:idemp:"
CALLBACK_PREFIX = "wfo:cb:"


def idempotency_key(process_name: str, external_key: str) -> str:
    return f"{IDEMPOTENCY_PREFIX}{process_name}:{external_key}"


def step_lock_key(process_id: str, step_index: int) -> str:
    return f"{LOCK_PREFIX}proc:{process_id}:step:{step_index}"


def callback_lock_key(task_id: str) -> str:
    return f"{CALLBACK_PREFIX}{task_id}"


class LockBackend:
    async def acquire(self, key: str, ttl_s: int) -> bool:  # noqa: D401
        raise NotImplementedError

    async def release(self, key: str) -> None:
        raise NotImplementedError


class InMemoryLock(LockBackend):
    def __init__(self) -> None:
        self._locks: dict[str, float] = {}

    async def acquire(self, key: str, ttl_s: int) -> bool:
        now = time.time()
        exp = self._locks.get(key)
        if exp is None or exp < now:
            self._locks[key] = now + ttl_s
            return True
        return False

    async def release(self, key: str) -> None:
        self._locks.pop(key, None)


class RedisLock(LockBackend):

    def __init__(self, redis: Redis, value: Optional[str] = None) -> None:
        if redis is None:
            raise RuntimeError("Redis client is required for RedisLock")
        self.redis = redis
        self.value = value or "1"

    async def acquire(self, key: str, ttl_s: int) -> bool:
        return bool(await self.redis.set(key, self.value, ex=ttl_s, nx=True))

    async def release(self, key: str) -> None:
        try:
            await self.redis.delete(key)
        except Exception:
            pass


async def ensure_idempotent_start(
    lock: LockBackend,
    process_name: str,
    external_key: str,
    ttl_s: int = 600,
) -> bool:
    key = idempotency_key(process_name, external_key)
    return await lock.acquire(key, ttl_s)


async def ensure_step_once(
    lock: LockBackend,
    process_id: str,
    step_index: int,
    ttl_s: int = 3600,
) -> bool:
    key = step_lock_key(process_id, step_index)
    return await lock.acquire(key, ttl_s)


async def dedupe_callback(
    lock: LockBackend,
    task_id: str,
    ttl_s: int = 3600,
) -> bool:
    key = callback_lock_key(task_id)
    return await lock.acquire(key, ttl_s)