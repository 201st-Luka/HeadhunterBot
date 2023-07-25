from interactions import slash_command, SlashCommandOption, OptionType, Extension, Client, SlashContext, Permissions, SlashCommandChoice, \
    User, SlashCommand, AutoDefer
from pyclasher import PlayerRequest, ClanRequest
from pyclasher.models import ApiCodes

from Bot.Exceptions import InvalidClanTag, InvalidPlayerTag, AlreadyLinkedPlayerTag
from Bot.HeadhunterBot import HeadhunterClient
from Bot.Extensions.player.linking import player_linking_info


class SudoCommand(Extension):
    client: HeadhunterClient

    def __init__(self, client: HeadhunterClient):
        self.client = client

    sudo = SlashCommand(
        name="sudo",
        default_member_permissions=Permissions.ADMINISTRATOR,
        auto_defer=AutoDefer(enabled=True)
    )

    user = sudo.group(
        name="user"
    )

    @user.subcommand(
        sub_cmd_name="force_link_player",
        sub_cmd_description="force links a player account to a Discord account",
        options=[
            SlashCommandOption(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            SlashCommandOption(
                name="player",
                description="linked players or search player by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def force_link_player(self, ctx: SlashContext, user: User, player_tag: str) -> None:
        try:
            player = await PlayerRequest(player_tag).request()
        except ApiCodes.NOT_FOUND:
            raise InvalidPlayerTag
        if player_tag in self.client.db_user.users.fetch_player_tags(user.id):
            raise AlreadyLinkedPlayerTag
        self.client.db_user.users.insert_user(user.id, player.tag, player.name)
        await ctx.send(f"The player {player.name} ({player.tag}) was linked to the user {user.username}.")

    @user.subcommand(
        sub_cmd_name="force_unlink_player",
        sub_cmd_description="force unlinks a player account from a Discord account",
        options=[
            SlashCommandOption(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            SlashCommandOption(
                name="player",
                description="enter their player tag",
                type=OptionType.STRING,
                required=True
            )
        ]
    )
    async def force_unlink_player(self, ctx: SlashContext, user: User, player: str) -> None:
        player_list = self.client.db_user.users.fetch_all_players_of_user(user.id)
        player_tag_list = [player_elem[1] for player_elem in player_list]
        if player in player_tag_list:
            pos = player_tag_list.index(player)
            self.client.db_user.users.delete_user_player(user.id, player)
            await ctx.send(f"The player {player_list[pos][0]} ({player_list[pos][1]}) was unliked from the account "
                           f"{user.username}.")
        else:
            await ctx.send(f"The player tag {player} is not linked to {user.username}."
                           f"Use `/sudo user show_players_accounts` first.")

    @user.subcommand(
        sub_cmd_name="show_players_accounts",
        sub_cmd_description="shows linked ClashOfClans accounts of a player",
        options=[
            SlashCommandOption(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            )
        ]
    )
    async def show_players_accounts(self, ctx: SlashContext, user: User) -> None:
        await player_linking_info(ctx, self.client.db_user, user)

    guild = sudo.group(name="guild")

    @guild.subcommand(
        sub_cmd_name="link_clan",
        sub_cmd_description="sets the clan tag for your guild",
        options=[
            SlashCommandOption(
                name="clan",
                description="search a clan and get the tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_clan(self, ctx: SlashContext, clan_tag: str) -> None:
        response_clan = await ClanRequest(clan_tag).request()
        if 'reason' not in response_clan:
            self.client.db_user.guilds.update_clan_tag_and_name(ctx.guild_id, response_clan.tag, response_clan.name)
            await ctx.send(f"The clan for this guild was successfully set to {response_clan.name} ({response_clan.tag}).")
        raise InvalidClanTag

    @guild.subcommand(
        sub_cmd_name="unset_clan",
        sub_cmd_description="unsets the clan tag from your guild"
    )
    async def unset_clan(self, ctx: SlashContext) -> None:
        if self.client.db_user.guilds.fetch_clantag(ctx.guild_id) is not None:
            self.client.db_user.guilds.update_clan_tag_and_name(ctx.guild_id, None, None)
            await ctx.send("The clan tag was removed.")
        else:
            await ctx.send("There is no clan tag set for this guild, so it cannot be removed.")

    @guild.subcommand(
        sub_cmd_name="info_clan",
        sub_cmd_description="shows the linked clan tag of your guild"
    )
    async def info_clan(self, ctx: SlashContext) -> None:
        clan_tag = self.client.db_user.guilds.fetch_clantag(ctx.guild_id)
        if clan_tag is not None:
            await ctx.send(f"The clan tag for this guild is {clan_tag}.")
        else:
            await ctx.send("There is no clan tag for this guild. You can set is using `/sudo guild link_clan <clan_tag>`.")

    clan_members = sudo.group(name="clan_members")

    @clan_members.subcommand(
        sub_cmd_name="feed",
        sub_cmd_description="clan member feed configuration",
        options=[
            SlashCommandOption(
                name="channel",
                description="when a player joins, leaves the clan, ... a message is send in this channel",
                type=OptionType.CHANNEL,
                required=False
            ),
            SlashCommandOption(
                name="status",
                description="on or off",
                type=OptionType.BOOLEAN,
                required=False,
            )
        ]
    )
    async def feed(self, ctx: SlashContext, **kwargs) -> None:
        await ctx.send(str(kwargs))
        raise NotImplementedError

    @clan_members.subcommand(
        sub_cmd_name="blacklist",
        sub_cmd_description="player blacklist of players that are not welcome in the clan",
        options=[
            SlashCommandOption(
                name="player_tag",
                description="search player by tag",
                type=OptionType.STRING,
                required=False,
                autocomplete=True
            ),
            SlashCommandOption(
                name="dc_user",
                description="all ClashOfClans accounts linked to this player",
                type=OptionType.USER,
                required=False
            )
        ]
    )
    async def blacklist(self, ctx: SlashContext, **kwargs) -> None:
        await ctx.send(str(kwargs))
        raise NotImplementedError

    @slash_command(
        name="clear",
        description="clears the chat",
        default_member_permissions=Permissions.ADMINISTRATOR,
        options=[SlashCommandOption(name="message_amount",
                                    description="the amount of messages to delete",
                                    type=OptionType.INTEGER,
                                    required=True)
                 ]
    )
    async def clear(self, ctx: SlashContext, message_amount: int) -> None:
        await ctx.defer()
        await ctx.channel.purge(message_amount)
        await ctx.send(f"Deleted {message_amount} messages.", ephemeral=True)


def setup(client: HeadhunterClient) -> None:
    SudoCommand(client)
