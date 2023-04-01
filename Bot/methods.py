import asyncio
import logging
from typing import Optional, Coroutine, Any

import aiohttp
from interactions import CommandContext, ComponentContext

from Bot.exceptions import NoClanTagLinked, NoPlayerTagLinked, InvalidClanTag, InvalidPlayerTag
from API.Clans.clan import Clan
from API.Players.player import Player
from Database.user import User


class Methods:
    def __init__(self):
        self.player = Player()
        self.clan = Clan()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def check_player_tag(self, player_tag: Optional[str] = None, ctx: Optional[CommandContext] = None,
                         user: Optional[User] = None) -> Coroutine[Any, Any, str | Coroutine[Any, Any, str]]:
        async def get_check_player_tag(player_tag: Optional[str] = None, ctx: Optional[CommandContext] = None,
                                       user: Optional[User] = None) -> str | Coroutine[Any, Any, str]:
            async with self:
                if not player_tag and ctx and user:
                    player_tag = user.users.fetch_player_tags(ctx.guild_id)
                if not player_tag:
                    raise NoPlayerTagLinked("No player tag linked")
                stripped_player_tag = player_tag.strip("#")
                response = self.player.player(stripped_player_tag)
                if response == {"reason": "notFound"}:
                    raise InvalidPlayerTag("Invalid player tag")
                return player_tag

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_check_player_tag(player_tag, ctx, user))
        return get_check_player_tag(player_tag, ctx, user)

    def check_clan_tag(self, clan_tag: Optional[str] = None, ctx: Optional[CommandContext] = None,
                       user: Optional[User] = None) -> Coroutine[Any, Any, str | Coroutine[Any, Any, str]]:
        async def get_check_clan_tag(clan_tag: Optional[str] = None, ctx: Optional[CommandContext] = None,
                                     user: Optional[User] = None) -> str | Coroutine[Any, Any, str]:
            async with self:
                if not clan_tag and ctx and user:
                    clan_tag = user.guilds.fetch_clantag(ctx.guild_id)
                if not clan_tag:
                    raise NoClanTagLinked("No clan tag linked")
                stripped_clan_tag = clan_tag.strip("#")
                response = self.clan.clan(stripped_clan_tag)
                if response == {"reason": "notFound"}:
                    raise InvalidClanTag("Invalid clan tag")
                return clan_tag

        if asyncio.get_running_loop() is None:
            return asyncio.run(get_check_clan_tag(clan_tag, ctx, user))
        return get_check_clan_tag(clan_tag, ctx, user)

    @staticmethod
    def command_wrapper(command):
        async def wrapper(ctx: CommandContext, *args, **kwargs):
            logging.info(
                f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.id}) used /{command.__name__} on guild '{ctx.guild}' "
                f"({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}).")
            try:
                await command(ctx, *args, **kwargs)
            except NoClanTagLinked:
                await ctx.send("This guild doesn't have a linked clan tag. Do `/linkclan <clan tag>` first!")
            except InvalidClanTag:
                await ctx.send("Your entered clan tag is not valid!")
            except NoPlayerTagLinked:
                await ctx.send("You don't have a linked player tag. Do `/linkplayer <player tag>` first!")
            except InvalidPlayerTag:
                await ctx.send("Your entered player tag is not valid!")

            except Exception as exception:
                await ctx.send(
                    f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                    f"{str(exception)}```")
                raise

        return wrapper

    @staticmethod
    def component_wrapper(component_callback):
        async def wrapper(ctx: ComponentContext, *args, **kwargs):
            logging.info(
                f"The user {ctx.user.username}#{ctx.user.discriminator} ({ctx.id}) used the component {component_callback.__name__} on guild '{ctx.guild}' "
                f"({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}).")
            try:
                await component_callback(ctx, *args, **kwargs)
            except Exception as e:
                logging.error(
                    f"Error in executing component {component_callback.__name__} by user {ctx.user.username}#{ctx.user.discriminator} ({ctx.id}) on guild '{ctx.guild}' ({ctx.guild_id}) in channel '{ctx.channel}' ({ctx.channel_id}): {e}"
                )
                raise e

        return wrapper

    @staticmethod
    def get_achievement_completion_info(json, index: int):
        return json['achievements'][index]['completionInfo'].split(" ")[-1]

    @staticmethod
    def clans_of_clans_and_tag(kwargs_):
        if 'clans' in kwargs_:
            clans = kwargs_['clans']
        elif 'clan' in kwargs_:
            clans = kwargs_['clan']
        else:
            clans = kwargs_

        if isinstance(clans, dict):
            return [clans, '']
        else:
            return [clans[:len(clans) - len(clans.split(" ")[-1]) - 1],
                    clans[len(clans) - len(clans.split(" ")[-1]):]]
