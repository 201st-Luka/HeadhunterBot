[![Discord][discord_shield]][discord_url]

# HeadhunterBot

This project is a Discord bot written in Python. It retrieves information about a player, clan, war and so on and sends it as a formatted message (as an Embed for example) in the chat.

---

## The bot

The discord bot communicated with the ClashOfClans api and sends information about a request (trough a user command) in the chat.

The bot is written in Python because I started programming with this language and the bot is also my first project. There is also a good api for Discord and its interactions.

###### Problems

The old discord-py library god outdated and hasn't god any updates because of a Discord based decision, so I had to rewrite the whole project for another library which got a huge update and I had to rewrite it again.

###### Future features

I plan some huge features in the future like

- a way to give detailed statistics for a player
- track the activity of a player
- automatic updates for the statistics I have to implement first
- a wiki page

I am open for new suggestions and ideas for features (or write them by yourself and create a pull request)

---

## Installation of the repository

1. Firstly, you have to copy the repository to your machine.
2. Secondly, you have to install the following libraries:

   - [interactions](interactions_docs) (`pip install -U discord-py-interactions`)
   - [coloredlogs](coloredLogs_docs) (`pip install coloredlogs`)

3. Then, you have to register a Discord bot on the official Discord site. You can do this [here](discord_developers). You have to manually copy the token in the `Bot/Variables.py` file to the `discordApiToken` variable.
4. Lastly, you have to create a ClashOfClans api key. You have to go to the [official ClashOfClans site](clashOfClans_site). Copy the token and paste it in the `Bot/Variables.py` file and replace in the `clashOfClansHeaders` dict the authorisation bearer.

You're done. Happy coding.

---

# What I DISALLOW to do

I don't want that my bot gets copied and hosted on a server. I am going to set up a server to host the bot soon. So If you want any custom features, please contact me via Discord or create a pull request with your implementation of the feature.

I don't want that anyone steals my project and makes money with it trough ads, ... .



<!---links--->
[interactions_docs]: https://interactionspy.readthedocs.io/en/latest/#
[coloredLogs_docs]: https://coloredlogs.readthedocs.io/en/latest/
[discord_developers]: https://discord.com/developers/applications
[clashOfClans_site]: https://developer.clashofclans.com/#/
[discord_shield]: https://img.shields.io/badge/Discord-blue?logo=discord&logoColor=white
[discord_url]: https://discord.gg/j2PAF9Wru8
