from interactions import Extension, SlashCommand, SlashContext

from Bot.HeadhunterBot import HeadhunterClient
from Bot.Interactions.SlashCommandOptions import MemberOption


class ActivityCommand(Extension):
    def __init__(self, client: HeadhunterClient):
        self.client = client

    activity = SlashCommand(name="activity")
    clan = activity.group(name="clan")

    @clan.subcommand(
        sub_cmd_name="member",
        sub_cmd_description="returns information about one member of the linked clan",
        options=[
            MemberOption
        ]
    )
    async def member(self, ctx: SlashContext, member: str) -> None:
        await ctx.send(member)

    @clan.subcommand(
        sub_cmd_name="members",
        sub_cmd_description="returns information about the linked clan's members"
    )
    async def members(self, ctx: SlashContext) -> None:
        await ctx.send("...")


def setup(client: HeadhunterClient) -> None:
    ActivityCommand(client)
