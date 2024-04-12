import itertools
import hashlib

import argon2


def solve_argon2(
    salt: str, secret: str, difficulty: int, time_cost: int, memory_cost: int
) -> int:
    prefix = "0" * difficulty
    for i in itertools.count():
        hashed = argon2.low_level.hash_secret_raw(
            secret=f"{secret}{i}".encode("utf-8"),
            salt=salt.encode("utf-8"),
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=1,
            hash_len=32,
            type=argon2.low_level.Type.ID,
        )
        if hashed.hex().startswith(prefix):
            return i


def solve_sha256(salt: str, secret: str, difficulty: int) -> int:
    # w
    prefix = "0" * difficulty
    secret = f"{salt}{secret}"
    for i in itertools.count():
        hashed = hashlib.sha256(f"{secret}{i}".encode("utf-8"))
        if hashed.hexdigest().startswith(prefix):
            return i
