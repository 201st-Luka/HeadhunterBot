from typing import Annotated

from interactions import SlashCommand, SlashCommandOption, OptionType, SlashContext, Extension
from pyclasher import PlayerRequest

from Bot.Interactions.Converters import PlayerTagConverter
from Bot.Exceptions import AlreadyLinkedPlayerTag, NoPlayerTagLinked
from Bot.Extensions.player.linking import player_linking_info
from Bot.HeadhunterBot import HeadhunterClient


class PlayerCommand(Extension):
    def __init__(self, client: HeadhunterClient):
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
    async def link_add(self, ctx: SlashContext, player: Annotated[PlayerRequest, PlayerTagConverter]) -> None:
        if player.tag in self.client.db_user.users.fetch_player_tags(ctx.user.id):
            raise AlreadyLinkedPlayerTag
        self.client.db_user.users.insert_user(ctx.user.id, player.tag, player.name)
        await ctx.send(f"The player {player.name} ({player.tag}) was successfully linked to you.")

    @link.subcommand(
        sub_cmd_name="info",
        sub_cmd_description="shows the linked players"
    )
    async def link_info(self, ctx: SlashContext) -> None:
        await player_linking_info(ctx, self.client.db_user, ctx.user)

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
    async def link_remove(self, ctx: SlashContext, player: Annotated[PlayerRequest, PlayerTagConverter]) -> None:
        player_tags = self.client.db_user.users.fetch_player_tags(ctx.user.id)
        if not len(player_tags):
            raise NoPlayerTagLinked
        if player not in player_tags:
            await ctx.send(f"The player with the tag {player} is not linked to your account.")
            return

        name = self.client.db_user.users.fetch_user_player_tag_name(ctx.author_id, player.tag)
        self.client.db_user.users.delete_user_player(ctx.user.id, player)
        await ctx.send(f"The player {name} ({player}) was removed.")


def setup(client: HeadhunterClient) -> None:
    PlayerCommand(client)
