from interactions import CommandContext, Embed

from Bot.Exeptions import InvalidClanTag, AlreadyLinkedClanTag, NoClanTagLinked
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

async def unset_clan(ctx: CommandContext, user: User):
    clan_and_tag = user.guilds.fetch_clanname_and_tag(ctx.guild_id)
    if clan_and_tag != (None, None):
        user.guilds.update_clan_tag_and_name(ctx.guild_id, None, None)
        player_embed = Embed(
            title=f"Deleted {clan_and_tag[0]} (#{clan_and_tag[1]})",
            description=f"Successfully unset **{clan_and_tag[0]}** (#{clan_and_tag[1]}) from this guild."
        )
        await ctx.send(embeds=player_embed)
        return
    raise NoClanTagLinked

async def info_clan(ctx: CommandContext, user: User):
    clan_and_tag = user.guilds.fetch_clanname_and_tag(ctx.guild_id)
    if clan_and_tag != (None, None):
        clan_embed = Embed(
            title=f"Linked clan for {ctx.guild.name}",
            description=f"You have **{clan_and_tag[0]}** (#{clan_and_tag[1]}) linked."
        )
        await ctx.send(embeds=clan_embed)
        return
    raise NoClanTagLinked


