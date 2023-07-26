class NoClanTagLinked(Exception):
    def __int__(self):
        pass


class NoPlayerTagLinked(Exception):
    def __int__(self):
        pass


class InvalidClanTag(Exception):
    def __int__(self):
        pass


class InvalidPlayerTag(Exception):
    def __int__(self):
        pass


class AlreadyLinkedClanTag(Exception):
    def __int__(self):
        pass


class AlreadyLinkedPlayerTag(Exception):
    def __int__(self):
        pass


class InitialisationError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key
        return

    def __str__(self) -> str:
        return f"The key '{self.key}' must be an environment variable."
