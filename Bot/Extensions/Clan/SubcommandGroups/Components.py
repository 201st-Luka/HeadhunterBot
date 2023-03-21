from interactions import ComponentContext, Embed, ActionRow, Button, ButtonStyle, CommandContext

from CocApi.Clans.Clan import clan
from CocApi.Clans.Clanwar import war_log
from Bot.Variables import wars_per_page as wars_p_page


async def publish_warlog_embed(ctx: CommandContext | ComponentContext, clan_tag: str, page: int, edit: bool):
    clan_response = await clan(clan_tag)
    warlog_json = await war_log(clan_tag)
    warlog_response = [war_clan for war_clan in warlog_json['items'] if war_clan['attacksPerMember'] == 2]
    max_pages = [(len(warlog_response) // wars_p_page) + 1 if len(warlog_response) % wars_p_page else len(warlog_response) // wars_p_page][0]
    page = [1 if page <= 0 else max_pages if page > max_pages else page][0]
    start, end = (page - 1) * wars_p_page, page * wars_p_page
    clan_embed = Embed(
        title=f"Warlog of {clan_response['name']} #{clan_tag}",
        description=f"war frequency: **{clan_response['warFrequency']}**\n"
                    f"war win streak: **{clan_response['warWinStreak']}**\n"
                    f"wins - losses- ties: **{clan_response['warWins']}** - **{clan_response['warLosses']}** - **{clan_response['warTies']}**\n"
                    f"war league: **{clan_response['warLeague']['name']}**"
    )
    clan_embed.set_thumbnail(clan_response['badgeUrls']['large'])
    clan_embed.set_footer(f"Page {page} of {max_pages}")
    page_wars = warlog_response[start:end]
    [clan_embed.add_field(
        name=f"__{clan_war['clan']['name']} ({clan_war['clan']['clanLevel']}) vs {clan_war['opponent']['name']} ({clan_war['opponent']['clanLevel']})__",
        value=f"Result: **{clan_war['result']}**\n"
              f"End date and time: **{clan_war['endTime'][6:8]}"
              f"{['st' if clan_war['endTime'][7] == '1' else 'nd' if clan_war['endTime'][7] == '2' else 'rd' if clan_war['endTime'][7] == '3' else 'th'][0]} "
              f"{['January' if clan_war['endTime'][4:6] == '01' else 'February' if clan_war['endTime'][4:6] == '02' else 'March' if clan_war['endTime'][4:6] == '03' else 'April' if clan_war['endTime'][4:6] == '04' else 'May' if clan_war['endTime'][4:6] == '05' else 'June' if clan_war['endTime'][4:6] == '06' else 'July' if clan_war['endTime'][4:6] == '07' else 'August' if clan_war['endTime'][4:6] == '08' else 'September' if clan_war['endTime'][4:6] == '09' else 'October' if clan_war['endTime'][4:6] == '10' else 'November' if clan_war['endTime'][4:6] == '11' else 'December'][0]} {clan_war['endTime'][0:4]}"
              f"** at {clan_war['endTime'][9:11]}:{clan_war['endTime'][11:13]}\n"
              f"Team size: **{clan_war['teamSize']}**\n"
              f"Attacks: **{clan_war['clan']['attacks']}** of {clan_war['teamSize'] * 2}\n"
              f"Stars: **{clan_war['clan']['stars']}** - **{clan_war['opponent']['stars']}**\n"
              f"Destruction percentage: **{str(clan_war['clan']['destructionPercentage'])[:5]}** - **{str(clan_war['opponent']['destructionPercentage'])[:5]}**\n"
              f"XP earned: **{clan_war['clan']['expEarned']}**"
    ) for clan_war in page_wars]
    if edit:
        await ctx.edit(embeds=clan_embed,
                       components=ActionRow(components=[
                           Button(
                               style=ButtonStyle.PRIMARY,
                               label="Previous page",
                               custom_id="button_warlog_command_previous_page",
                               disabled=[True if page == 1 else False][0]
                           ), Button(
                               style=ButtonStyle.SECONDARY,
                               label="Next page",
                               custom_id="button_warlog_command_next_page",
                               disabled=[False if page != max_pages else True][0]
                           )
                       ]))
        return
    await ctx.send(embeds=clan_embed,
                   components=ActionRow(components=[
                       Button(
                           style=ButtonStyle.PRIMARY,
                           label="Previous page",
                           custom_id="button_warlog_command_previous_page",
                           disabled=[True if page == 1 else False][0]
                       ), Button(
                           style=ButtonStyle.SECONDARY,
                           label="Next page",
                           custom_id="button_warlog_command_next_page",
                           disabled=[False if page != max_pages else True][0]
                       )
                   ]))
    return


async def warlog_previous_page(ctx: ComponentContext):
    clan_tag = ctx.message.embeds[0].title.split(' ')[-1].strip('#')
    page = int(ctx.message.embeds[0].footer.text.split(" ")[1]) - 1
    await publish_warlog_embed(ctx, clan_tag, page, True)
    return

async def warlog_next_page(ctx: ComponentContext):
    clan_tag = ctx.message.embeds[0].title.split(' ')[-1].strip('#')
    page = int(ctx.message.embeds[0].footer.text.split(" ")[1]) + 1
    await publish_warlog_embed(ctx, clan_tag, page, True)
    return
