from interactions import SlashContext, User as InteractionsUser, Embed
from pyclasher.bulk_requests import PlayerBulkRequest
from pyclasher.models.Enums import ClanRole

from Database.user import User as DbUser


class Linking:
    async def player_linking_info(self, ctx: SlashContext, db_user: DbUser,
                                  interactions_user: InteractionsUser) -> None:
        player_tags = db_user.users.fetch_player_tags(interactions_user.id)
        embed = Embed(
            title=f"Player accounts for {interactions_user.username}#{interactions_user.discriminator}",
            description=f"{interactions_user.username}#{interactions_user.discriminator} possesses {len(player_tags)} {'account' if len(player_tags) == 1 else 'accounts'}",
        )
        if not len(player_tags):
            await ctx.send(embeds=embed)
        player_responses = await PlayerBulkRequest(player_tags).request()
        for player_response in player_responses[0:25]:
            if 'reason' in player_response:
                embed.add_field(
                    name=f"No information for {player_response.tag}",
                    value="N/A"
                )
            else:
                embed.add_field(
                    name=f"__{player_response.name} ({player_response.tag})__",
                    value=f"Clan: **{player_response.clan.name}**\n"
                          f"Role: **{'Leader' if player_response.role == ClanRole.LEADER else 'Co-leader' if player_response.role == ClanRole.COLEADER else 'Elder' if player_response.role == ClanRole.ADMIN else 'Member'}**\n"
                          f"Town hall level: **{player_response.town_hall_level}**\n"
                          f"Trophies: **{player_response.trophies}**"
                )
        await ctx.send(embeds=embed)
