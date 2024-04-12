from urllib.parse import urlparse
import requests
from .utils import solve_argon2, solve_sha256
from .exceptions import ChallengeRequestError


class BasedSession(requests.Session):
    """A session that can solve BasedFlare challenges automatically."""

    def __init__(self):
        super().__init__()
        self.solvers = {
            "argon2": solve_argon2,
            # sha256 does not require the same parameters as argon2 (time_cost, memory_cost)
            # but BasedFlare sends them anyway, so we have to wrap it to keep the same parser
            "sha256": lambda salt, secret, difficulty, *args: solve_sha256(
                salt, secret, difficulty
            ),
        }

    def request(self, method, url, **kwargs):
        domain = urlparse(url).netloc
        # Solve the challenge if the session does not have the necessary cookie
        if not self.cookies.get(
            "_basedflare_pow", domain=f".{domain}"
        ) and not url.endswith(".basedflare/bot-check"):
            self.__solve_challenge(domain)

        res = super().request(method, url, **kwargs)

        # Fallback to solving the challenge if the response is a redirect, e.g. the cookie is invalid
        if ".basedflare/bot-check?/" in res.url:
            self.__solve_challenge(domain)
            res = super().request(method, url, **kwargs)

        return res

    def __solve_challenge(self, domain):
        challenge = self.__get_challenge(domain)
        if challenge["ca"]:
            raise NotImplementedError("CAPTCHA challenges are not supported")

        algorithm, params = challenge["pow"].split("#", 1)
        if algorithm not in self.solvers:
            raise NotImplementedError(f"{algorithm} is not a supported algorithm")

        solution = self.solvers[algorithm](
            *challenge["ch"].split("#")[0:2], *map(int, params.split("#"))
        )
        self.__post_challenge(domain, f"{challenge['ch']}#{solution}")

    def __get_challenge(self, domain):
        res = self.get(
            f"https://{domain}/.basedflare/bot-check",
            headers={"Accept": "application/json"},
        )
        if res.status_code != requests.codes.forbidden:
            raise ChallengeRequestError(
                f"Unexpected status code {res.status_code} when fetching the challenge"
            )

        return res.json()

    def __post_challenge(self, domain, pow_response):
        res = self.post(
            f"https://{domain}/.basedflare/bot-check",
            data={"pow_response": pow_response},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if res.status_code != requests.codes.found:
            raise ChallengeRequestError(
                f"Unexpected status code {res.status_code} when posting the challenge solution"
            )
        if "_basedflare_pow" not in res.headers.get("Set-Cookie", ""):
            raise ChallengeRequestError(
                "The server did not send the bypass cookie after solving the challenge"
            )
