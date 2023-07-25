from typing import Annotated
from interactions import Client, SlashCommand, SlashCommandOption, OptionType, SlashContext, Extension

from Bot.Converters.PyClasher import PlayerConverter
from Bot.Extensions.player.linking import Linking
from Bot.Exceptions import InvalidPlayerTag, AlreadyLinkedPlayerTag, NoPlayerTagLinked
from Database.user import User


class PlayerCommand(Extension):
    client: Client

    def __init__(self, client: Client):
        self.player_linking = Linking()
        self.client = client

    player = SlashCommand(name="player", description="returns information about a player")

    link = player.group(name="link")

    @link.subcommand(
        sub_cmd_name="add",
        sub_cmd_description="link a ClashOfClans account to your Discord account",
        options=[
            SlashCommandOption(
                name="player",
                description="enter or search a player tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_add(self, ctx: SlashContext, player_tag: str = None) -> None:
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

    @link.subcommand(
        sub_cmd_name="info",
        sub_cmd_description="shows the linked players"
    )
    async def link_info(self, ctx: SlashContext) -> None:
        await self.player_linking.player_linking_info(ctx, self.user, ctx.user)

    @link.subcommand(
        sub_cmd_name="remove",
        sub_cmd_description="remove a player",
        options=[
            SlashCommandOption(
                name="player",
                description="linked players",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_remove(self, ctx: SlashContext, player: str) -> None:
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
    async def player_tag(self, ctx: SlashContext, input_str: str = "") -> None:
        await self.auto_completes.player_tag_auto_complete(ctx, self.user, input_str)

    @player.autocomplete("player")
    async def player_autocomplete(self, ctx: SlashContext, input_str: str = "") -> None:
        await self.auto_completes.player_auto_complete(ctx, self.user, input_str)


def setup(client: Client) -> None:
    PlayerCommand(client)
