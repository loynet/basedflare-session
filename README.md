# basedflare-session

A package that
extends [Python's requests session](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) to solve
some [BasedFlare](https://basedflare.com/) Proof of Work (PoW) challenges automatically.
It also includes utility functions to solve the challenges manually.

Please note that **this package is a work in progress** and may not function in all cases.
Currently, it supports the `argon2` and `sha256` PoW challenges.
Any other challenge, such as a CAPTCHA, will raise an exception.

## Usage

Suppose `example.com` is a website that requires you to solve a challenge before you can access it. Below is a simple
example of how to use the package:

```python
from basedflare_session import BasedSession

# Create a new session
session = BasedSession()

# Use the session to send a GET request
response = session.get('https://example.com')

# Print the response
print(response.text)
```