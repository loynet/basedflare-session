"""
The basedflare-session package provides a requests-flavored session to solve BasedFlare challenges automatically.
It also includes utility functions to solve the challenges manually.
"""

from .session import BasedSession
from .utils import solve_argon2, solve_sha256

__all__ = ["BasedSession", "solve_argon2", "solve_sha256"]
