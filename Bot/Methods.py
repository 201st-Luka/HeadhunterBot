import logging
from interactions import CommandContext, ComponentContext

from Bot.Exeptions import NoClanTagLinked, InvalidClanTag, InvalidPlayerTag, NoPlayerTagLinked, InvalidCommandSyntax
from CocApi.Clans.Clan import clan
from CocApi.Players.PLayer import player
from Database.User import User


def check_clan_tag(clan_tag: str, ctx: CommandContext, user: User) -> str:
    if clan_tag is None:
        clan_tag = user.guilds.fetch_clantag(ctx.guild_id)
        if clan_tag is None:
            raise NoClanTagLinked
        return clan_tag
    if clan_tag.startswith("#"):
        clan_tag = clan_tag.strip("#")
    response_clan = clan(clan_tag)
    if response_clan == {"reason": "notFound"}:
        raise InvalidClanTag
    del response_clan
    return clan_tag


def check_player_tag(player_tag: str, ctx: CommandContext, user: User) -> str:
    if player_tag is None:
        player_tag = user.users.fetch_player_tags(ctx.author.id)
        if player_tag is None:
            raise NoPlayerTagLinked
        return player_tag
    if player_tag.startswith("#"):
        player_tag = player_tag.strip("#")
    response_player = player(player_tag)
    if response_player == {"reason": "notFound"}:
        raise InvalidPlayerTag
    del response_player
    return player_tag


def command_wrapper(command):
    async def wrapper(ctx: CommandContext, *args, **kwargs):
        # logging ----------------
        logging.info(f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.id}) used /{command.__name__} on guild '{ctx.guild}' "
                     f"({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}).")
        try:
            # mother command -----
            await command(ctx, *args, **kwargs)
            return
        # exceptions -------------
        except NoClanTagLinked:
            await ctx.send("This guild doesn't have a linked clan tag. Do `/linkclan <clan tag>` first!")
            return
        except InvalidClanTag:
            await ctx.send("Your entered clan tag is not valid!")
            return
        except NoPlayerTagLinked:
            await ctx.send("You don't have a linked player tag. Do `/linkplayer <player tag>` first!")
            return
        except InvalidPlayerTag:
            await ctx.send("Your entered player tag is not valid!")
            return
        except InvalidCommandSyntax:
            await ctx.send("Your entered command doesn't follow the supported syntax!")
        except Exception as exception:
            await ctx.send(
                f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                f"{str(exception)}```")
            raise

    return wrapper


def component_wrapper(component_callback):
    async def wrapper(ctx: ComponentContext, *args, **kwargs):
        # logging ----------------
        logging.info(f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.id}) used the component {component_callback.__name__} on guild '{ctx.guild}' "
                     f"({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}).")
        try:
            # mother component callback
            await component_callback(ctx, *args, **kwargs)
            return
        # exceptions -------------
        except InvalidClanTag:
            await ctx.send("Your entered clan tag is not valid!")
            return
        except InvalidPlayerTag:
            await ctx.send("Your entered player tag is not valid!")
            return
        except Exception as exception:
            await ctx.send(
                f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                f"{str(exception)}```")
            raise

    return wrapper


def get_achievement_completion_info(json, index: int):
    return json['achievements'][index]['completionInfo'].split(" ")[-1]


def kwargs2clan_and_tag(kwargs_):
    if 'clans' in kwargs_:
        return [kwargs_['clans'][:len(kwargs_['clans']) - len(kwargs_['clans'].split(" ")[-1]) - 1],
                kwargs_['clans'][len(kwargs_['clans']) - len(kwargs_['clans'].split(" ")[-1]):]]
    elif 'clan' in kwargs_:
        return [kwargs_['clan'][:len(kwargs_['clan']) - len(kwargs_['clan'].split(" ")[-1]) - 1],
                kwargs_['clan'][len(kwargs_['clan']) - len(kwargs_['clan'].split(" ")[-1]):]]


