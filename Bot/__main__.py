from pyclasher import Missing

from .HeadhunterBot import HeadhunterClient


def Missing__str__(self) -> str:
    return "N/A"


Missing.__str__ = Missing__str__


# main
headhunter_bot = HeadhunterClient("config.json")
headhunter_bot.load_extensions()

headhunter_bot.start()
