from interactions import CommandContext, User as InteractionsUser, Embed

from CocApi.Players.Player import player_bulk
from Database.User import User as DbUser


async def player_linking_info(
        ctx: CommandContext,
        db_user: DbUser,
        interactions_user: InteractionsUser
) -> None:
    player_tags = db_user.users.fetch_player_tags(interactions_user.id)
    embed = Embed(
        title=f"Player accounts for {interactions_user.username}#{interactions_user.discriminator}",
        description=f"{interactions_user.username}#{interactions_user.discriminator} possesses {len(player_tags)} {'account' if len(player_tags) == 1 else 'accounts'}",
    )
    if not len(player_tags):
        await ctx.send(embeds=embed)
        return
    player_responses = await player_bulk(player_tags)
    for player_response in player_responses[0:25]:
        if 'reason' in player_response:
            embed.add_field(
                name=f"No information for {player_response['tag']}",
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
