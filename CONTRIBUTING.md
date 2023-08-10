# Contributing

Contributing to this open-source project is appreciated. To contribute please visit the Discord server as well.

---

## Where to start

The contribution starts with an issue. The created issue should explain what to do. Based on this issue you can start
contributing. If so, refer to the issue in the pull request. 

### Issues

The issues must follow these guidelines:
- An issue must not be a duplicate of an existing issue.
- A bug issue must provide clear information about the bug.
- A feature request should contain information about how to implement the feature (for example what slash commands
  should be created and how they should be called)

Irrelevant issues, duplicates or issues failing to comply to these guidelines will be closed. 

### Pull requests

After solving the issue it is possible to create a pull request. This pull request must target the `master` branch. From 
there it will be part of the bot in the next release.

Requirements for a pull request are:
- Commits must be clear
- The pull request must be up-to-date with the `master` branch
- All checks (if applicable) must pass
- A review must be requested from at least one developer (Puvude and 201st-Luka)

### Recognising the contribution

When the PR is merged in the `master` branch. GitHub will automatically add the user to the repository's contributor
list. It is also possible to earn a role on the Discord server for contribution.

---

## Installation

To install HeadhunterBot, follow these steps:

1. Copy the repository to your local machine:
   ```bash
   git clone https://github.com/201st-Luka/HeadhunterBot.git
   ```
2. Install the requirements: 
   - [interactions](https://pypi.org/project/discord-py-interactions/) (`pip install -U interactions.py`) 
   - [coloredlogs](https://pypi.org/project/coloredlogs/) (`pip install coloredlogs`)
   - [pyclasher](https://github.com/201st-Luka/PyClasher.git@v1.0.0-alpha1) (`pip install git+https://github.com/201st-Luka/PyClasher.git@v1.0.0-alpha1`)
   
   by simply running
   
   ```bash
   pip install -r requirements.txt
   ```
3. Register a Discord bot on the official Discord site [here](https://discord.com/developers/applications):
   Create a new app, go to the "Bot" section and copy the Bot token. 

   You have to create an environment variable called `DISCORD_TOKEN` on your run environment and assign the copied value
   to it (for PyCharm users simply go to the run configuration, browse `run.py` as file to run and add the environment
   variable in the "Environment variables" tab). 
4. Create a ClashofClans API key on the [official ClashOfClans site](https://developer.clashofclans.com/#/) here. Copy the token and create a new 
   environment variable named `CLASHOFCLANS_TOKENS` and use the copied token as its value. You can use multiple tokens,
   the separator is `:`.
5. It is also important to specify the destination of the logs and the database. To do that, simply create 2 environment
   variables called `LOG_PATH` and `DB_PATH` for the log folder and the database. 
6. If you want to test your custom features, you can also specify a debug scope for your testing server. Create a last
   environment variable and assign the server ID to `DEBUG_SCOPE`. This is optional and is not required (but recommended
   for testing and debugging).
7. Run the HeadhunterBot for the first time: this will create the database and the log files and folder. The bot should
   start running and logging to you that the bot successfully logged in.

You're done! Happy coding.

---
