from interactions import Client, extension_command, Option, OptionType, CommandContext, Extension, Choice, Embed

from Bot.Exeptions import InvalidPlayerTag, AlreadyLinkedPlayerTag, NoPlayerTagLinked
from Bot.Extensions.Utils.autocompletes import player_tag_auto_complete, player_auto_complete
from CocApi.Players.Player import player as player_request, player_bulk
from Database.User import User


class PlayerCommand(Extension):
    client: Client
    user: User

    def __init__(self, client: Client, user: User):
        self.client = client
        self.user = user
        return

    @extension_command(
        name="player",
        description="returns information about a player",
        default_scope=True,
    )
    async def player(self, ctx: CommandContext):
        pass

    @player.group(name="link")
    async def link(self, ctx: CommandContext):
        pass

    @link.subcommand(
        name="add",
        description="link a ClashOfClans account to your Discord account",
        options=[
            Option(
                name="player_tag",
                description="enter or search a player tag",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_add(self, ctx: CommandContext, player_tag: str):
        if player_tag[0] != '#':
            player_tag = "".join(('#', player_tag))
        response_player = await player_request(player_tag)
        if 'reason' in response_player:
            raise InvalidPlayerTag
        if player_tag in self.user.users.fetch_player_tags(ctx.user.id):
            raise AlreadyLinkedPlayerTag
        self.user.users.insert_user(ctx.user.id, response_player['tag'], response_player['name'])
        await ctx.send(f"The player {response_player['name']} ({response_player['tag']}) was successfully linked to you.")
        return

    @link.subcommand(
        name="info",
        description="shows the linked players"
    )
    async def link_info(self, ctx: CommandContext):
        player_tags = self.user.users.fetch_player_tags(ctx.user.id)
        if len(player_tags) == 0:
            await ctx.send("You don't have any linked players. Do `/player link add <player_tag>` first.")
            return
        player_responses = await player_bulk(player_tags)
        embed = Embed(
            title=f"Player accounts for {ctx.user.username}#{ctx.user.discriminator}",
            value=f"{ctx.user.username} possesses {len(player_tags)} {'account' if len(player_tags) == 1 else 'accounts'}",
        )
        for player_response, player_tag in zip(player_responses[0:25], player_tags[0:25]):
            if 'reason' in player_response:
                embed.add_field(
                    name=f"No information for {player_tag}",
                    value="N/A"
                )
            else:
                embed.add_field(
                    name=f"{player_response['name']} ({player_response['tag']})",
                    value=f"Clan: **{player_response['clan']['name']}**\n"
                          f"Role: **{'Leader' if player_response['role'] == 'leader' else 'Co-leader' if player_response['role'] == 'coLeader' else 'Elder' if player_response['role'] == 'admin' else 'Member'}**\n"
                          f"Town hall level: **{player_response['townHallLevel']}**\n"
                          f"Trophies: **{player_response['trophies']}**"
                )
        await ctx.send(embeds=embed)
        return

    @link.subcommand(
        name="remove",
        description="remove a player",
        options=[
            Option(
                name="player",
                description="linked players",
                type=OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ]
    )
    async def link_remove(self, ctx: CommandContext, player: str):
        if player[0] != '#':
            player = "".join(('#', player))
        player_tags = self.user.users.fetch_player_tags(ctx.user.id)
        if len(player_tags) == 0:
            raise NoPlayerTagLinked
        if player not in player_tags:
            await ctx.send(f"The player with the tag {player} is not linked to your account.")
            return
        name = self.user.users.fetch_user_player_tag_name
        self.user.users.delete_user_player(ctx.user.id, player)
        await ctx.send(f"The player {name} ({player}) was removed.")
        return

    @player.autocomplete("player_tag")
    async def player_tag(self, ctx: CommandContext, input_str: str = ""):
        await player_tag_auto_complete(ctx, self.user, input_str)
        return

    @player.autocomplete(name="player")
    async def player_autocomplete(self, ctx: CommandContext, input_str: str = ""):
        await player_auto_complete(ctx, self.user, input_str)
        return


def setup(client: Client, user: User):
    PlayerCommand(client, user)
    return
