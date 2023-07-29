from typing import Annotated

from interactions import slash_command, SlashCommandOption, OptionType, Extension, Client, SlashContext, Permissions, \
    SlashCommandChoice, User, SlashCommand, AutoDefer, ChannelType, GuildChannel
from pyclasher import PlayerRequest, ClanRequest
from pyclasher.models import ApiCodes

from Bot.Exceptions import InvalidClanTag, InvalidPlayerTag, AlreadyLinkedPlayerTag
from Bot.HeadhunterBot import HeadhunterClient
from Bot.Interactions.Converters import ClanTagConverter, PlayerTagConverter
from Bot.Interactions.SlashCommandOptions import ClanOption, PlayerOption


class SudoCommand(Extension):
    client: HeadhunterClient

    def __init__(self, client: HeadhunterClient):
        self.client = client

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
    async def blacklist(self, ctx: SlashContext) -> None:
        await ctx.send("not implemented yet")
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
