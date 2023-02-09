from interactions import Client, extension_command, Option, OptionType, CommandContext, Extension

from Bot.Extensions.Extensionssetup import extension_command_wrapper
from Bot.Methods import check_player_tag
from CocApi.Players.Player import player
from Database.User import User
from Database.Data_base import DataBase


class Player(Extension):
    client: Client
    user: User = User(DataBase())

    def __init__(self, client: Client):
        self.client = client
        return

    @extension_command(
        name="player",
        description="returns information about a player",
        default_scope=True,
        options=[Option(name="player_tag",
                        description="enter your player tag here",
                        type=OptionType.STRING,
                        required=False)
                 ]
    )
    @extension_command_wrapper
    async def player(self, ctx: CommandContext, player_tag=None):
        player_tag = await check_player_tag(player_tag, ctx, self.user)
        response_player = await player(player_tag)
        await ctx.send(f"information of {response_player['name']} #{player_tag}")
        return


def setup(client: Client):
    Player(client)
    return
