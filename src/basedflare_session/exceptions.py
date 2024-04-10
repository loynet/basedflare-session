class ChallengeRequestError(Exception):
    """Exception raised when some challenge request fails."""

    def __init__(self, message="Challenge request failed"):
        self.message = message
        super().__init__(self.message)
