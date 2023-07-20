from Bot.HeadhunterBot import HeadhunterClient


if __name__ == '__main__':
    headhunter_bot = HeadhunterClient("config.json")
    # headhunter_bot.load_extensions()

    headhunter_bot.start()
