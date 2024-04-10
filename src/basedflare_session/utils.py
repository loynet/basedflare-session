import itertools

import argon2


def solve_argon2(salt: str, secret: str, difficulty: int, time_cost: int, memory_cost: int) -> int:
    prefix = '0' * difficulty
    for i in itertools.count():
        hashed = argon2.low_level.hash_secret_raw(
            secret=f"{secret}{i}".encode('utf-8'),
            salt=salt.encode('utf-8'),
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=1,
            hash_len=32,
            type=argon2.low_level.Type.ID
        )
        if hashed.hex().startswith(prefix):
            return i
