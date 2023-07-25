from interactions import slash_command, SlashCommandOption, OptionType, Extension, Client, SlashContext, Permissions, SlashCommandChoice, \
    User as InteractionsUser

from Bot.Extensions.Player.linking import Linking
from Bot.Extensions.Utils.auto_completes import AutoCompletes
from Bot.Exceptions import InvalidClanTag, InvalidPlayerTag, AlreadyLinkedPlayerTag
from API.Clans.clan import Clan
from API.Players.player import Player
from Database.user import User as DbUser


class SudoCommand(Extension):
    client: Client

    def __init__(self, client: Client, user: DbUser):
        self.player_linking = Linking()
        self.auto_completes = AutoCompletes()
        self.player = Player()
        self.clan = Clan()
        self.client = client
        self.user = user

    @slash_command(
        name="sudo",
        default_scope=True,
        default_member_permissoins=Permissions.ADMINISTRATOR
    )
    async def sudo(self, ctx: SlashContext, **kwargs) -> None:
        await ctx.defer()
        return

    @sudo.group(
        name="user"
    )
    async def user(self, ctx: SlashContext) -> None:
        pass

    @user.subcommand(
        name="force_link_player",
        description="force links a player account to a Discord account",
        options=[
            SlashCommandOption(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            SlashCommandOption(
                name="player_tag",
                description="linked players or search player by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def force_link_player(self, ctx: SlashContext, user: InteractionsUser, player_tag: str) -> None:
        if player_tag[0] != '#':
            player_tag = "".join(('#', player_tag))
        player_response = await self.player.player(player_tag)
        if 'reason' in player_response:
            raise InvalidPlayerTag
        if player_tag in self.user.users.fetch_player_tags(user.id):
            raise AlreadyLinkedPlayerTag
        self.user.users.insert_user(user.id, player_response['tag'], player_response['name'])
        await ctx.send(
            f"The player {player_response['name']} ({player_response['tag']}) was linked to the user {user.username}.")

    @user.subcommand(
        name="force_unlink_player",
        description="force unlinks a player account from a Discord account",
        options=[
            SlashCommandOption(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            SlashCommandOption(
                name="their_player_tag",
                description="enter their player tag",
                type=OptionType.STRING,
                required=True
            )
        ]
    )
    async def force_unlink_player(self, ctx: SlashContext, user: InteractionsUser, their_player_tag: str) -> None:
        player_list = self.user.users.fetch_all_players_of_user(user.id)
        if their_player_tag[0] != '#':
            their_player_tag = "".join(('#', their_player_tag))
        player_tag_list = [player_elem[1] for player_elem in player_list]
        if their_player_tag in player_tag_list:
            pos = player_tag_list.index(their_player_tag)
            self.user.users.delete_user_player(user.id, their_player_tag)
            await ctx.send(f"The player {player_list[pos][0]} ({player_list[pos][1]}) was unliked from the account "
                           f"{user.username}#{user.discriminator}.")
        else:
            await ctx.send(f"The player tag {their_player_tag} is not linked to {user.username}#{user.discriminator}. "
                           f"Use `/sudo user show_players_accounts` first.")

    @user.subcommand(
        name="show_players_accounts",
        description="shows linked ClashOfClans accounts of a player",
        options=[
            SlashCommandOption(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            )
        ]
    )
    async def show_players_accounts(self, ctx: SlashContext, user: InteractionsUser) -> None:
        await self.player_linking.player_linking_info(ctx, self.user, user)

    @sudo.group(name="guild")
    async def guild(self, ctx: SlashContext) -> None:
        pass

    @guild.subcommand(
        name="link_clan",
        description="sets the clan tag for your guild",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="search a clan and get the tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_clan(self, ctx: SlashContext, clan_tag: str) -> None:
        if clan_tag[0] != '#':
            clan_tag = "".join(('#', clan_tag))
        response_clan = await self.clan.clan(clan_tag)
        if 'reason' not in response_clan:
            self.user.guilds.update_clan_tag_and_name(ctx.guild_id, response_clan['tag'], response_clan['name'])
            await ctx.send(
                f"The clan for this guild was successfully set to {response_clan['name']} ({response_clan['tag']}).")
        raise InvalidClanTag

    @guild.subcommand(
        name="unset_clan",
        description="unsets the clan tag from your guild"
    )
    async def unset_clan(self, ctx: SlashContext) -> None:
        if self.user.guilds.fetch_clantag(ctx.guild_id) is not None:
            self.user.guilds.update_clan_tag_and_name(ctx.guild_id, None, None)
            await ctx.send("The clan tag was removed.")
        else:
            await ctx.send("There is no clan tag set for this guild, so it cannot be removed.")

    @guild.subcommand(
        name="info_clan",
        description="shows the linked clan tag of your guild"
    )
    async def info_clan(self, ctx: SlashContext) -> None:
        clan_tag = self.user.guilds.fetch_clantag(ctx.guild_id)
        if clan_tag is not None:
            await ctx.send(f"The clan tag for this guild is {clan_tag}.")
        else:
            await ctx.send(
                "There is no clan tag for this guild. You can set is using `/sudo guild link_clan <clan_tag>`.")

    @sudo.group(name="clan_members")
    async def clan_members(self, ctx: SlashContext) -> None:
        pass

    @clan_members.subcommand(
        name="feed",
        description="clan member feed configuration",
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

    @clan_members.subcommand(
        name="blacklist",
        description="player blacklist of players that are not welcome in the clan",
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

    @slash_command(
        name="clear",
        description="clears the chat",
        default_scope=True,
        default_member_permissoins=Permissions.ADMINISTRATOR,
        options=[SlashCommandOption(name="message_amount",
                        description="the amount of messages to delete",
                        type=OptionType.INTEGER,
                        required=True)
                 ]
    )
    async def clear(self, ctx: SlashContext, message_amount: int) -> None:
        await ctx.channel.typing
        await ctx.channel.purge(message_amount)
        await ctx.send(f"Deleted {message_amount} messages.", ephemeral=True)

    @sudo.autocomplete("player_tag")
    async def player_tag_autocomplete(self, ctx: SlashContext, input_str: str = None) -> None:
        await self.auto_completes.player_tag_auto_complete(ctx, self.user, input_str)

    @sudo.autocomplete("clan_tag")
    async def clan_tag(self, ctx: SlashContext, input_str: str = None) -> None:
        if input_str is None:
            await ctx.populate([])
        choices = []
        clan_tag_response = await self.clan.clan(input_str)
        if clan_tag_response != {'reason': 'notFound'}:
            choices.append(SlashCommandChoice(
                name=f"{clan_tag_response['name']} {clan_tag_response['tag']}, "
                     f"Lvl: {clan_tag_response['clanLevel']}, "
                     f"Location: {clan_tag_response['location']['name']}, "
                     f"{clan_tag_response['members']}/50",
                value=str(clan_tag_response['tag'])
            ))
        if len(input_str) > 3:
            clan_search_response = await self.clan.clan_search(input_str, 10)
            if len(clan_search_response['items']) > 0:
                search_choices = [SlashCommandChoice(
                    name=f"{c['name']} {c['tag']}, "
                         f"Lvl: {c['clanLevel']}, "
                         f"Location: {c['location']['name'] if 'location' in c else 'n/a'}, "
                         f"{c['members']}/50",
                    value=str(c['tag'])
                ) for c in clan_search_response['items']]
                choices += search_choices
        await ctx.populate(choices)


def setup(client: Client, user: DbUser) -> None:
    SudoCommand(client, user)
