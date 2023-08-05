from typing import Annotated

from interactions import slash_command, SlashCommandOption, OptionType, Extension, SlashContext, Permissions, \
    SlashCommand, ChannelType, GuildChannel, Embed, Color, Modal, ParagraphText, \
    ModalContext
from interactions.ext.paginators import Paginator
from pyclasher import PlayerRequest, ClanRequest

from Bot.Exceptions import InvalidClanTag, InvalidPlayerTag
from Bot.HeadhunterBot import HeadhunterClient
from Bot.Interactions.Converters import ClanTagConverter, PlayerTagConverter
from Bot.Interactions.SlashCommandOptions import ClanOption, PlayerOption


class SudoCommand(Extension):
    client: HeadhunterClient

    def __init__(self, client: HeadhunterClient):
        self.client = client
        return

    sudo = SlashCommand(
        name="sudo",
        default_member_permissions=Permissions.ADMINISTRATOR
    )

    guild = sudo.group(name="guild")

    @guild.subcommand(
        sub_cmd_name="link_clan",
        sub_cmd_description="sets the clan tag for your guild",
        options=[
            ClanOption
        ]
    )
    async def link_clan(self, ctx: SlashContext, clan: Annotated[ClanRequest, ClanTagConverter]) -> None:
        self.client.db_user.guilds.update_clan_tag_and_name(ctx.guild_id, clan.tag, clan.name)
        await ctx.send(f"The clan for this guild was successfully linked to {clan.name} ({clan.tag}).")
        return

    @link_clan.error
    async def on_link_clan_error(self, exception: Exception, ctx: SlashContext, clan: str = None) -> None:
        if isinstance(exception, InvalidClanTag):
            await ctx.send(str(InvalidClanTag(clan)), ephemeral=True)
        return

    @guild.subcommand(
        sub_cmd_name="unset_clan",
        sub_cmd_description="unsets the clan tag from your guild"
    )
    async def unset_clan(self, ctx: SlashContext) -> None:
        if self.client.db_user.guilds.fetch_clantag(ctx.guild_id) is not None:
            self.client.db_user.guilds.update_clan_tag_and_name(ctx.guild_id, None, None)
            await ctx.send("The clan tag was removed.")
        else:
            await ctx.send("There is no clan tag set for this guild so it cannot be removed.")

    @guild.subcommand(
        sub_cmd_name="info_clan",
        sub_cmd_description="shows the linked clan tag of your guild"
    )
    async def info_clan(self, ctx: SlashContext) -> None:
        clan_tag = self.client.db_user.guilds.fetch_clantag(ctx.guild_id)
        if clan_tag is not None:
            await ctx.send(f"The clan tag for this guild is {clan_tag}.")
        else:
            await ctx.send("There is no clan tag for this guild. You can set is using "
                           "`/sudo guild link_clan <clan_tag>`.")

    feed = sudo.group(name="feed")

    @feed.subcommand(
        sub_cmd_name="members",
        sub_cmd_description="clan member feed configuration",
        options=[
            SlashCommandOption(
                name="channel",
                description="when a player joins, leaves the clan, ... a message is send in this channel",
                type=OptionType.CHANNEL,
                channel_types=[
                    ChannelType.GUILD_TEXT,
                    ChannelType.GUILD_NEWS,
                    ChannelType.GUILD_NEWS_THREAD,
                    ChannelType.GUILD_PRIVATE_THREAD,
                    ChannelType.GUILD_PUBLIC_THREAD
                ],
                required=False
            )
        ]
    )
    async def members(self, ctx: SlashContext, channel: GuildChannel = None) -> None:
        if channel is None:
            feed_channel_id = self.client.db_user.guilds.fetch_feed_channel(ctx.guild_id)
            if feed_channel_id is None:
                await ctx.send("There is no linked clan feed channel. You can do this by using "
                               "`/sudo feed members <channel>`.")
                return

            channel = await self.client.fetch_channel(feed_channel_id)
            await ctx.send(f"The linked clan feed channel is {channel.mention}.")
            return

        self.client.db_user.guilds.update_feed_channel(ctx.guild_id, channel.id)
        await ctx.send(f"Successfully linked the feed channel to {channel.mention}.")
        return

    blacklist = sudo.group(name="blacklist")

    @blacklist.subcommand(
        sub_cmd_name="info",
        sub_cmd_description="player blacklist of players that are not welcome in the clan",
    )
    async def info(self, ctx: SlashContext) -> None:
        black_list = self.client.db_user.guild_blacklist.fetch_players(ctx.guild_id)

        if not len(black_list):
            await ctx.send("The blacklist for this guild is empty.")
            return

        embeds: list[Embed] = []

        for start in range(0, len(black_list), self.client.cfg['players_per_page']):
            embed = Embed(
                title=f"Blacklist for {ctx.guild.name}",
                description=f"{ctx.guild.name} has {len(black_list)} account"
                            f"{'' if len(black_list) == 1 else 's'} on the blacklist",
                color=Color.from_hex(self.client.cfg['embed_color'].strip('0x') if
                                     self.client.cfg['embed_color'].startswith('0x') else
                                     self.client.cfg['embed_color'])
            )

            for player in black_list[start:start + self.client.cfg['players_per_page']]:
                embed.add_field(
                    name=f"__{player[1]} ({player[0]})__",
                    value=f"__Reason__: {player[2] if player[2] is not None else 'not provided'}"
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

    @blacklist.subcommand(
        sub_cmd_name="add",
        sub_cmd_description="add a player to the guild blacklist",
        options=[
            PlayerOption
        ]
    )
    async def add(self, ctx: SlashContext, player: Annotated[PlayerRequest, PlayerTagConverter]) -> None:
        blacklist = self.client.db_user.guild_blacklist.fetch_players(ctx.guild_id)

        if not len(blacklist) or player.tag not in [row[0] for row in blacklist]:
            modal = Modal(
                ParagraphText(
                    label=f"Blacklisting {player.name} reason",
                    custom_id=f"{ctx.guild.id}_{player.tag}_modal_sudo_blacklist_add_label",
                    placeholder="Enter your reason for a ban or leave this field empty",
                    max_length=1500
                ),
                title="Reason"
            )

            await ctx.send_modal(modal)

            modal_ctx: ModalContext = await self.client.wait_for_modal(modal)

            reason = "N/A"
            if (response := modal_ctx.responses[f'{ctx.guild.id}_{player.tag}_modal_sudo_blacklist_add_label']) != "":
                reason = response

            self.client.db_user.guild_blacklist.insert_player(ctx.guild_id, player.tag, player.name,
                                                              response if response != "" else None)

            await modal_ctx.send(content=f"Added **{player.name}** {player.tag} to the blacklist. Reason:\n*"
                                         f"{reason}*")
            return

        else:
            reason = 'N/A'
            for sublist in blacklist:
                if sublist[0] == player.tag and sublist[2] is not None:
                    reason = sublist[2]
            await ctx.send(f"The player {player.name} {player.tag} is already on the blacklist. Reason:\n*{reason}*")
            return

    @add.error
    async def on_add_error(self, exception: Exception, ctx: SlashContext, player: str = None) -> None:
        if isinstance(exception, InvalidPlayerTag):
            await ctx.send(str(InvalidPlayerTag(player)), ephemeral=True)
        return

    @slash_command(
        name="clear",
        description="clears the chat",
        default_member_permissions=Permissions.ADMINISTRATOR,
        options=[SlashCommandOption(
            name="message_amount",
            description="the amount of messages to delete",
            type=OptionType.INTEGER,
            required=True
        )]
    )
    async def clear(self, ctx: SlashContext, message_amount: int) -> None:
        await ctx.defer()
        deleted = await ctx.channel.purge(message_amount)
        await ctx.send(f"Deleted {len(deleted) if isinstance(deleted, list) else deleted} messages.",
                       ephemeral=True)


def setup(client: HeadhunterClient) -> None:
    SudoCommand(client)
