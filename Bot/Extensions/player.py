from interactions import Client, extension_command, Option, OptionType, CommandContext, Extension, Choice

from Bot.Methods import check_player_tag
from CocApi.Clans.Clan import members
from CocApi.Players.Player import player
from Database.User import User


class Player(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.client = client
        self.user = user
        return

    @extension_command(
        name="player",
        description="returns information about a player",
        default_scope=True,
        options=[
            Option(
                name="player_tag",
                description="enter your player tag here",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def player(self, ctx: CommandContext, player_tag=None):
        player_tag = await check_player_tag(player_tag, ctx, self.user)
        response_player = await player(player_tag)
        await ctx.send(f"information of {response_player['name']} #{player_tag}")
        return

    @player.autocomplete("player_tag")
    async def player_tag(self, ctx: CommandContext, **kwargs):
        choices = []
        clan_tag = self.user.guilds.fetch_clantag(ctx.guild_id)
        if clan_tag != ():
            choices = [
                Choice(
                    name=f"{member['name']} {member['tag']}",
                    value=member['tag']
                ) for member in (await members(clan_tag))['items'][0:25]
            ]
        await ctx.populate(choices)


def setup(client: Client, user: User):
    Player(client, user)
    return
