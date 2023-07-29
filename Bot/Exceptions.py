from pyclasher.models import BaseClan


class HeadhunterException(Exception):
    def __str__(self) -> str:
        return "HeadhunterException"


class NoClanTagLinked(HeadhunterException):
    pass


class NoPlayerTagLinked(HeadhunterException):
    pass


class InvalidClanTag(HeadhunterException):
    def __init__(self, clan_tag: str = None) -> None:
        super().__init__()
        self.tag = clan_tag
        return

    def __str__(self) -> str:
        if hasattr(self, 'tag') and self.tag is not None:
            return (f"The provided clan tag '{self.tag}' is not a valid clan tag. Make sure that the tag starts with "
                    f"'#' and is existing in ClashOfClans.")
        return f"The provided clan tag is not a valid clan tag. Make sure that the tag starts with '#' " \
               f"and is existing in ClashOfClans."


class InvalidPlayerTag(HeadhunterException):
    pass


class AlreadyLinkedClanTag(HeadhunterException):
    pass


class AlreadyLinkedPlayerTag(HeadhunterException):
    pass


class InitialisationError(HeadhunterException):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key
        return

    def __str__(self) -> str:
        return f"The key '{self.key}' must be an environment variable."


class NotInWar(HeadhunterException):
    def __str__(self) -> str:
        return "This clan is not in a clan war"
