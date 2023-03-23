from interactions import extension_command, Option, OptionType, Extension, Client, CommandContext, Permissions, Choice, extension_autocomplete

from Bot.Exeptions import InvalidClanTag
from CocApi.Clans.Clan import members, clan, clan_search
from CocApi.Players.Player import player
from Database.User import User


class SudoCommand(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.client = client
        self.user = user
        return

    @extension_command(
        name="sudo",
        default_scope=True,
        default_member_permissoins=Permissions.ADMINISTRATOR
    )
    async def sudo(self, ctx: CommandContext, **kwargs):
        pass

    @sudo.group(
        name="user"
    )
    async def user(self, ctx: CommandContext):
        pass

    @user.subcommand(
        name="force_link_player",
        description="force links a player account to a Discord account",
        options=[
            Option(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            Option(
                name="player_tag",
                description="linked players or search player by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def force_link_player(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @user.subcommand(
        name="force_unlink_player",
        description="force unlinks a player account from a Discord account",
        options=[
            Option(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            ),
            Option(
                name="player_tag",
                description="linked players or search player by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def force_unlink_player(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @user.subcommand(
        name="show_players_accounts",
        description="shows linked ClashOfClans accounts of a player",
        options=[
            Option(
                name="user",
                description="guild user you want to execute the operation on",
                type=OptionType.USER,
                required=True
            )
        ]
    )
    async def show_players_accounts(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @sudo.group(
        name="guild"
    )
    async def guild(self, ctx: CommandContext):
        pass

    @guild.subcommand(
        name="link_clan",
        description="sets the clan tag for your guild",
        options=[
            Option(
                name="clan_tag",
                description="search a clan and get the tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_clan(self, ctx: CommandContext, clan_tag: str):
        if await clan(clan_tag) != {'reason': 'notFound'}:
            self.user.guilds.update_clan_tag(ctx.guild_id, clan_tag)
            await ctx.send(f"The clan tag for this guild was successfully set to {clan_tag}.")
            return
        raise InvalidClanTag

    @guild.subcommand(
        name="unset_clan",
        description="unsets the clan tag from your guild"
    )
    async def unset_clan(self, ctx: CommandContext):
        if self.user.guilds.fetch_clantag(ctx.guild_id) is not None:
            self.user.guilds.update_clan_tag(ctx.guild_id, None)
            await ctx.send("The clan tag was removed.")
        else:
            await ctx.send("There is no clan tag set for this guild, so it cannot be removed.")
        return

    @guild.subcommand(
        name="info_clan",
        description="shows the linked clan tag of your guild"
    )
    async def info_clan(self, ctx: CommandContext):
        clan_tag = self.user.guilds.fetch_clantag(ctx.guild_id)
        if clan_tag is not None:
            await ctx.send(f"The clan tag for this guild is {clan_tag}.")
        else:
            await ctx.send("There is no clan tag for this guild. You can set is using `/sudo guild link_clan <clan_tag>`.")
        return

    @sudo.group(
        name="clan_members"
    )
    async def clan_members(self, ctx: CommandContext):
        pass

    @clan_members.subcommand(
        name="feed",
        description="clan member feed configuration",
        options=[
            Option(
                name="channel",
                description="when a player joins, leaves the clan, ... a message is send in this channel",
                type=OptionType.CHANNEL,
                required=False
            ),
            Option(
                name="status",
                description="on or off",
                type=OptionType.BOOLEAN,
                required=False,
            )
        ]
    )
    async def feed(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @clan_members.subcommand(
        name="blacklist",
        description="player blacklist of players that are not welcome in the clan",
        options=[
            Option(
                name="player_tag",
                description="search player by tag",
                type=OptionType.STRING,
                required=False,
                autocomplete=True
            ),
            Option(
                name="dc_user",
                description="all ClashOfClans accounts linked to this player",
                type=OptionType.USER,
                required=False
            )
        ]
    )
    async def blacklist(self, ctx: CommandContext, **kwargs):
        await ctx.send(str(kwargs))
        return

    @extension_command(
        name="clear",
        description="clears the chat",
        default_scope=True,
        default_member_permissoins=Permissions.ADMINISTRATOR,
        options=[Option(name="message_amount",
                        description="the amount of messages to delete",
                        type=OptionType.INTEGER,
                        required=True)
                 ]
    )
    async def clear(self, ctx: CommandContext, message_amount: int):
        await ctx.channel.typing
        await ctx.channel.purge(message_amount)
        await ctx.send(f"Deleted {message_amount} messages.", ephemeral=True)
        return

    @sudo.autocomplete("player_tag")
    async def player_tag_autocomplete(self, ctx: CommandContext, *args):
        choices = []
        if args != ():
            arg0 = args[0].strip('#') if args[0].startswith('#') else args[0]
            clan_tag = self.user.guilds.fetch_clantag(ctx.guild_id)
            clan_members = await members(clan_tag)
            for clan_member in clan_members['items']:
                if arg0 in clan_member['name'] or arg0 in clan_member['tag']:
                    choices.append(Choice(
                        name=f"{clan_member['name']} ({clan_member['tag']})",
                        value=" ".join((clan_member['name'], clan_member['tag']))
                    ))
            if len(choices) == 0:
                player_response = await player(arg0)
                if player_response != {"reason": "notFound"}:
                    choices.append(Choice(
                        name=f"{player_response['name']} ({player_response['tag']})",
                        value=" ".join((player_response['name'], player_response['tag']))
                    ))
        await ctx.populate(choices)
        return

    @sudo.autocomplete("clan_tag")
    async def clan_tag(self, ctx: CommandContext, input_str: str = None):
        if input_str is None:
            await ctx.populate([])
            return
        choices = []
        clan_tag_response = await clan(input_str.strip('#') if input_str.startswith('#') else input_str)
        if clan_tag_response != {'reason': 'notFound'}:
            choices.append(Choice(
                name=f"{clan_tag_response['name']} {clan_tag_response['tag']}, "
                     f"Lvl: {clan_tag_response['clanLevel']}, "
                     f"Location: {clan_tag_response['location']['name']}, "
                     f"{clan_tag_response['members']}/50",
                value=str(clan_tag_response['tag'])
            ))
        if len(input_str) > 3:
            clan_search_response = await clan_search(input_str, 10)
            if len(clan_search_response['items']) > 0:
                search_choices = [Choice(
                        name=f"{c['name']} {c['tag']}, "
                             f"Lvl: {c['clanLevel']}, "
                             f"Location: {c['location']['name'] if 'location' in c else 'n/a'}, "
                             f"{c['members']}/50",
                        value=str(c['tag'])
                    ) for c in clan_search_response['items']]
                choices += search_choices
        await ctx.populate(choices)
        return


def setup(client: Client, user: User):
    SudoCommand(client, user)
    return


