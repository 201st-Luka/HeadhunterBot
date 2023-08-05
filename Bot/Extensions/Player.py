from typing import Annotated

from interactions import SlashCommand, SlashContext, Extension, Embed, Color
from interactions.ext.paginators import Paginator
from pyclasher import PlayerRequest
from pyclasher.models.Enums import ClanRole, ApiCodes

from Bot.Exceptions import AlreadyLinkedPlayerTag, NoPlayerTagLinked, InvalidPlayerTag
from Bot.HeadhunterBot import HeadhunterClient
from Bot.Interactions.Converters import PlayerTagConverter
from Bot.Interactions.SlashCommandOptions import PlayerOption


class PlayerCommand(Extension):
    def __init__(self, client: HeadhunterClient):
        self.client = client
        return

    player = SlashCommand(name="player", description="returns information about a player")

    link = player.group(name="link")

    @link.subcommand(
        sub_cmd_name="add",
        sub_cmd_description="link a ClashOfClans account to your Discord account",
        options=[
            PlayerOption
        ]
    )
    async def add(self, ctx: SlashContext, player: Annotated[PlayerRequest, PlayerTagConverter]) -> None:
        if player.tag in self.client.db_user.users.fetch_player_tags(ctx.user.id):
            raise AlreadyLinkedPlayerTag
        self.client.db_user.users.insert_user(ctx.user.id, player.tag, player.name)
        await ctx.send(f"The player {player.name} ({player.tag}) was successfully linked to you.")
        return

    @add.error
    async def on_add_error(self, exception: Exception, ctx: SlashContext, player: str) -> None:
        if isinstance(exception, InvalidPlayerTag):
            await ctx.send(str(InvalidPlayerTag(player)), ephemeral=True)
        if isinstance(exception, AlreadyLinkedPlayerTag):
            await ctx.send(str(AlreadyLinkedPlayerTag(player)), ephemeral=True)
        return

    @link.subcommand(
        sub_cmd_name="info",
        sub_cmd_description="shows the linked players"
    )
    async def info(self, ctx: SlashContext) -> None:
        player_tags = self.client.db_user.users.fetch_player_tags(ctx.user.id)

        if not len(player_tags):
            await ctx.send(f"The user {ctx.user.display_name} has no linked players.", ephemeral=True)
            return

        embeds: list[Embed] = []

        for start in range(0, len(player_tags), self.client.cfg['players_per_page']):
            embed = Embed(
                title=f"Player accounts for {ctx.user.display_name}",
                description=f"{ctx.user.display_name} has {len(player_tags)} account"
                            f"{'' if len(player_tags) == 1 else 's'}",
                color=Color.from_hex(self.client.cfg['embed_color'].strip('0x') if
                                     self.client.cfg['embed_color'].startswith('0x') else
                                     self.client.cfg['embed_color'])
            )

            for tag in player_tags[start:start + self.client.cfg['players_per_page']]:
                try:
                    player = await PlayerRequest(tag).request()
                except type(ApiCodes.NOT_FOUND.value):
                    embed.add_field(
                        name=f"No information for {tag}",
                        value="N/A"
                    )
                else:
                    embed.add_field(
                        name=f"__{player.name} ({player.tag})__",
                        value=f"Clan: **{player.clan.name}**\n"
                              f"Role: **{'Leader' if player.role == ClanRole.LEADER else 'Co-leader' if player.role == ClanRole.COLEADER else 'Elder' if (player.role == ClanRole.ADMIN) else 'Member'}**\n"
                              f"Town hall level: **{player.town_hall_level}**\n"
                              f"Trophies: **{player.trophies}**"
                    )

            embeds.append(embed)

        if len(embeds) == 1:
            await ctx.send(embeds=embeds)
            return

        paginator = Paginator.create_from_embeds(self.client, *embeds)
        paginator.default_color = Color.from_hex(self.client.cfg['embed_color'].strip('0x') if
                                                 self.client.cfg['embed_color'].startswith('0x') else
                                                 self.client.cfg['embed_color'])
        paginator.show_select_menu = True

        await paginator.send(ctx)
        return

    @link.subcommand(
        sub_cmd_name="remove",
        sub_cmd_description="remove a player",
        options=[
            PlayerOption
        ]
    )
    async def remove(self, ctx: SlashContext, player: Annotated[PlayerRequest, PlayerTagConverter]) -> None:
        player_tags = self.client.db_user.users.fetch_player_tags(ctx.user.id)
        if not len(player_tags):
            raise NoPlayerTagLinked
        if player.tag not in player_tags:
            await ctx.send(f"The player {player.name} ({player.tag}) is not linked to your account.")
            return

        self.client.db_user.users.delete_user_player(ctx.user.id, player.tag)
        await ctx.send(f"The player {player.name} ({player.tag}) was removed.")
        return

    @remove.error
    async def on_remove(self, exception: Exception, ctx: SlashContext, player: str) -> None:
        if isinstance(exception, InvalidPlayerTag):
            await ctx.send(str(InvalidPlayerTag(player)), ephemeral=True)
        return


def setup(client: HeadhunterClient) -> None:
    PlayerCommand(client)
