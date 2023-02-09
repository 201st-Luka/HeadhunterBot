from interactions import CommandContext, Embed

from Bot.Exeptions import InvalidClanTag, AlreadyLinkedClanTag
from CocApi.Clans.Clan import clan
from Database.User import User


async def set_clan(ctx: CommandContext, kwargs, user: User):
    if kwargs['tag'].startswith("#"):
        kwargs['tag'] = kwargs['tag'].strip("#")
    clan_response = await clan(kwargs['tag'])
    if clan_response == {"reason": "notFound"}:
        raise InvalidClanTag
    elif user.guilds.fetch_clantag(ctx.guild_id) != kwargs['tag']:
        user.guilds.update_clan_tag_and_name(ctx.guild_id, kwargs['tag'], clan_response['name'])
        clan_embed = Embed(
            title=f"Linked {kwargs['tag']}",
            description=f"Successfully linked **{clan_response['name']}** #{kwargs['tag']} to this server."
        )
        clan_embed.set_thumbnail(url=clan_response['badgeUrls']['large'])
        await ctx.send(embeds=clan_embed)
        return
    raise AlreadyLinkedClanTag
