[![Discord][discord_shield]][discord_url] ![Last commit][last_commit_shield]

# HeadhunterBot

HeadhunterBot is a Discord bot written in Python that retrieves information about a player, clan, war, and more. It sends the information as a formatted message in the chat, such as an embed.

---

## Features

- Retrieves information about a player, clan, war, and more from Clash of Clans API
- Written in Python with Discord API and interactions
- Open for suggestions and ideas for new features


###### Issues and Resolutions

The old `discord-py` library became outdated and stopped receiving updates due to a decision made by Discord. I had to rewrite the entire project for another library that had a major update, which presented its own set of challenges. However, the HeadhunterBot is now running smoothly with the updated library.

###### Planned Features

Here are some features that are planned for the future:

- Detailed statistics for players
- Activity tracking for players
- Automatic updates for statistics that have been implemented
- Wiki page for additional information

These features are aimed at improving the functionality and usefulness of the HeadhunterBot. Stay tuned for updates and progress on their development!

---

## Installation

To install HeadhunterBot, follow these steps:

1. Copy the repository to your local machine.
2. Install the following libraries: 
   - [interactions](https://pypi.org/project/discord-py-interactions/) (`pip install -U discord-py-interactions`) 
   - [coloredlogs](https://pypi.org/project/coloredlogs/) (`pip install coloredlogs`)
   
3. Register a Discord bot on the official Discord site [here](https://discord.com/developers/applications). Manually copy the token in the `Bot/Variables.py` file to the `discord_api_token` variable.
4. Create a ClashofClans API key on the [official ClashOfClans site](https://developer.clashofclans.com/#/) here. Copy the token and paste it in the `Bot/Variables.py` file, replacing the authorization bearer in the `clash_of_clans_headers` dict.
5. Run the Admin.py script once to create the database with all needed tables.
6. Lastly you have to run the `admin.py` script once to create the database with all needed tables.

You're done! Happy coding.


<!---links--->
[discord_shield]: https://img.shields.io/badge/Discord-blue?logo=discord&logoColor=white
[discord_url]: https://discord.gg/j2PAF9Wru8
[last_commit_shield]: https://img.shields.io/github/last-commit/201st-Luka/HeadhunterBot