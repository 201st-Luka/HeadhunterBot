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
        sub_cmd_description="returns information about the members of the linked clan",
        options=[
            MemberOption
        ]
    )
    async def members(self, ctx: SlashContext, member: str) -> None:
        await ctx.send(member)


def setup(client: HeadhunterClient) -> None:
    ActivityCommand(client)
