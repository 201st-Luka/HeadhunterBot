from interactions import Extension, Client, extension_command, CommandContext, Option, OptionType, Choice

from API.Clans.clan import Clan
from API.Clans.clan_war import ClanWar
from Database.user import User


class ActivityCommand(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.clan = Clan()
        self.clan_war = ClanWar()
        self.client = client
        self.user = user

    @extension_command()
    async def activity(self, ctx: CommandContext) -> None:
        pass

    @activity.subcommand(
        group="clan",
        name="members",
        description="returns information about the members of the linked clan",
        options=[
            Option(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]

    )
    async def members(self, ctx: CommandContext, **kwargs) -> None:
        await ctx.send(str(kwargs))

    @activity.autocomplete("clan_tag")
    async def clan_tag_autocomplete(self, ctx: CommandContext, *args) -> None:
        clans = [self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)]
        current_war_response = await self.clan_war.current_war(clans[0][1])
        if current_war_response['state'] != 'notInWar':
            clans.append((current_war_response['opponent']['name'], current_war_response['opponent']['tag'].strip("#")))
        if args != ():
            clan_response = await self.clan.clan(args[0].strip('#') if args[0].startswith('#') else args[0])
            if clan_response != {"reason": "notFound"}:
                clans.append((clan_response['name'], clan_response['tag'].strip("#")))
        choices = [Choice(name=f"{c[0]} (#{c[1]})", value=" ".join(c)) for c in clans]
        await ctx.populate(choices)


def setup(client: Client, user: User) -> None:
    ActivityCommand(client, user)
