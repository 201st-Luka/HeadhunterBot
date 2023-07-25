from interactions import Extension, SlashCommand, SlashContext, SlashCommandOption, OptionType, SlashCommandChoice
from Bot.HeadhunterBot import HeadhunterClient


class ActivityCommand(Extension):
    def __init__(self, client: HeadhunterClient):
        self.client = client

    activity = SlashCommand(name="activity")
    clan = activity.group(name="clan")

    @clan.subcommand(
        sub_cmd_name="members",
        sub_cmd_description="returns information about the members of the linked clan",
        options=[
            SlashCommandOption(
                name="clan_tag",
                description="linked clans and clan war opponent or search clan by tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]

    )
    async def members(self, ctx: SlashContext, **kwargs) -> None:
        await ctx.send(str(kwargs))

    @activity.autocomplete("clan_tag")
    async def clan_tag_autocomplete(self, ctx: SlashContext, *args) -> None:
        clans = [self.user.guilds.fetch_clanname_and_tag(ctx.guild_id)]
        current_war_response = await self.clan_war.current_war(clans[0][1])
        if current_war_response['state'] != 'notInWar':
            clans.append((current_war_response['opponent']['name'], current_war_response['opponent']['tag'].strip("#")))
        if args != ():
            clan_response = await self.clan.clan(args[0].strip('#') if args[0].startswith('#') else args[0])
            if clan_response != {"reason": "notFound"}:
                clans.append((clan_response['name'], clan_response['tag'].strip("#")))
        choices = [SlashCommandChoice(name=f"{c[0]} (#{c[1]})", value=" ".join(c)) for c in clans]
        await ctx.populate(choices)


def setup(client: HeadhunterClient) -> None:
    ActivityCommand(client)
