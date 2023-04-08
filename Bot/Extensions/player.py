from interactions import Client, extension_command, Option, OptionType, CommandContext, Extension

from Bot.Extensions.Player.linking import Linking
from Bot.Extensions.Utils.auto_completes import AutoCompletes
from Bot.exceptions import InvalidPlayerTag, AlreadyLinkedPlayerTag, NoPlayerTagLinked
from API.Players.player import Player
from Database.user import User


class PlayerCommand(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.player_linking = Linking()
        self.auto_completes = AutoCompletes()
        self.player = Player()
        self.client = client
        self.user = user

    @extension_command(name="player", description="returns information about a player", default_scope=True)
    async def player(self, ctx: CommandContext) -> None:
        pass

    @player.group(name="link")
    async def link(self, ctx: CommandContext) -> None:
        await ctx.defer()
        return

    @link.subcommand(
        name="add",
        description="link a ClashOfClans account to your Discord account",
        options=[
            Option(
                name="player_tag",
                description="enter or search a player tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_add(self, ctx: CommandContext, player_tag: str) -> None:
        if player_tag[0] != '#':
            player_tag = "".join(('#', player_tag))
        response_player = await self.player.player(player_tag)
        if 'reason' in response_player:
            raise InvalidPlayerTag
        if player_tag in self.user.users.fetch_player_tags(ctx.user.id):
            raise AlreadyLinkedPlayerTag
        self.user.users.insert_user(ctx.user.id, response_player['tag'], response_player['name'])
        await ctx.send(
            f"The player {response_player['name']} ({response_player['tag']}) was successfully linked to you.")

    @link.subcommand(name="info", description="shows the linked players")
    async def link_info(self, ctx: CommandContext) -> None:
        await self.player_linking.player_linking_info(ctx, self.user, ctx.user)

    @link.subcommand(
        name="remove",
        description="remove a player",
        options=[
            Option(
                name="player",
                description="linked players",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_remove(self, ctx: CommandContext, player: str) -> None:
        if player[0] != '#':
            player = "".join(('#', player))
        player_tags = self.user.users.fetch_player_tags(ctx.user.id)
        if len(player_tags) == 0:
            raise NoPlayerTagLinked
        if player not in player_tags:
            await ctx.send(f"The player with the tag {player} is not linked to your account.")

        name = self.user.users.fetch_user_player_tag_name
        self.user.users.delete_user_player(ctx.user.id, player)
        await ctx.send(f"The player {name} ({player}) was removed.")

    @player.autocomplete("player_tag")
    async def player_tag(self, ctx: CommandContext, input_str: str = "") -> None:
        await self.auto_completes.player_tag_auto_complete(ctx, self.user, input_str)

    @player.autocomplete(name="player")
    async def player_autocomplete(self, ctx: CommandContext, input_str: str = "") -> None:
        await self.auto_completes.player_auto_complete(ctx, self.user, input_str)


def setup(client: Client, user: User) -> None:
    PlayerCommand(client, user)
