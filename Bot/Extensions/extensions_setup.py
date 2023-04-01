from typing import Callable, Any, Coroutine

from interactions import CommandContext, Extension, ComponentContext

from Bot.exceptions import NoClanTagLinked, InvalidClanTag, NoPlayerTagLinked, InvalidPlayerTag, AlreadyLinkedClanTag


class ExtensionsSetup:

    @staticmethod
    def extension_command_wrapper(command) -> Callable[[Extension, CommandContext, tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
        async def extension_wrapper(extension: Extension, ctx: CommandContext, *args, **kwargs) -> None:
            try:
                await command(extension, ctx, *args, **kwargs)
            except NoClanTagLinked:
                await ctx.send("This guild doesn't have a linked clan tag. Do `/clan link set <clan tag>` first!")
            except InvalidClanTag:
                await ctx.send("Your entered clan tag is not valid!")
            except NoPlayerTagLinked:
                await ctx.send("You don't have a linked player tag. Do `/linkplayer <player tag>` first!")
            except InvalidPlayerTag:
                await ctx.send("Your entered player tag is not valid!")
            except AlreadyLinkedClanTag:
                await ctx.send("This clan has already been linked to this server")

            except Exception as exception:
                await ctx.send(
                    f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                    f"{str(exception)}```")
                raise

        return extension_wrapper

    @staticmethod
    def extension_component_wrapper(component_callback) -> Callable[[Extension, ComponentContext, tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, None]]:
        async def extension_wrapper(extension: Extension, ctx: ComponentContext, *args, **kwargs) -> None:
            try:
                await component_callback(extension, ctx, *args, **kwargs)
            except InvalidClanTag:
                await ctx.send("Your entered clan tag is not valid!")
            except InvalidPlayerTag:
                await ctx.send("Your entered player tag is not valid!")
            except Exception as exception:
                await ctx.send(
                    f"Something went wrong. Please report this error on my Discord server (`/dc`). Exception:\n```diff\n- "
                    f"{str(exception)}```")

        return extension_wrapper
